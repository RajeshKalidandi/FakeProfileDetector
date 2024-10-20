from fastapi import FastAPI, Depends, HTTPException, Request, Body, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from backend.models.user import User
from schemas import UserCreate, UserLogin, UserSchema, UserInDB
from services import freemium_service, user_service, auth_service, feature_toggle
from services.rate_limiter import rate_limiter
from typing import List
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import traceback
from pydantic import BaseModel
from bson import ObjectId
from firebase_admin import credentials, auth, initialize_app
from fastapi.responses import JSONResponse
from exceptions import AppError
from ml_models import FakeProfileDetector, extract_features, preprocess_data, train_model
from data_collection.collector import DataCollector
from fastapi import UploadFile
import json
import shutil

load_dotenv()  # Load environment variables from .env file

# Get the absolute path to the directory containing app.py
base_dir = os.path.abspath(os.path.dirname(__file__))

# Construct the path to the Firebase Admin SDK JSON file
firebase_config_path = os.path.join(base_dir, os.getenv('FIREBASE_ADMIN_SDK_PATH'))

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_config_path)
initialize_app(cred)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if not rate_limiter.check_rate_limit(request):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    response = await call_next(request)
    return response

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = User.verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user_dict = user.to_dict()
    user_dict['id'] = str(user_dict.pop('_id'))  # Convert ObjectId to string
    return UserInDB(**user_dict)

async def get_current_user_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserSchema)
async def register(user_data: UserCreate):
    try:
        user = auth_service.register_user(user_data.username, user_data.email, user_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user_dict = user.to_dict()
        user_dict['id'] = str(user_dict['_id'])  # Convert ObjectId to string
        del user_dict['_id']  # Remove the _id field
        return UserSchema(**user_dict)
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/api/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.login_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    access_token = User.generate_token(user['id'])
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.get("/api/auth/me", response_model=UserSchema)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    return UserSchema(**current_user.dict())

# Profile analysis endpoint
@app.post("/api/analyze/profile")
async def analyze_profile(
    profile_data: str = Form(...),
    profile_pictures: List[UploadFile] = File(None),
    current_user: UserInDB = Depends(get_current_user)
):
    if not freemium_service.check_scan_limit(current_user):
        raise HTTPException(status_code=403, detail="Daily scan limit reached")
    
    profile_data = json.loads(profile_data)
    
    # Save the uploaded images temporarily
    temp_image_paths = []
    if profile_pictures:
        for picture in profile_pictures:
            temp_image_path = f"temp_{picture.filename}"
            with open(temp_image_path, "wb") as buffer:
                shutil.copyfileobj(picture.file, buffer)
            temp_image_paths.append(temp_image_path)
        profile_data['profile_pictures'] = temp_image_paths
    
    features = extract_features(profile_data)
    model = FakeProfileDetector.load_model('trained_model.joblib')
    
    # Convert features dict to list in the correct order
    feature_list = [features[f] for f in model.feature_names_]
    
    prediction = model.predict([feature_list])[0]
    probability = model.predict_proba([feature_list])[0][1]  # Probability of being a fake profile

    freemium_service.increment_scan_count(current_user)
    
    # Remove the temporary image files
    for temp_path in temp_image_paths:
        os.remove(temp_path)
    
    return {
        "result": "fake" if prediction == 1 else "genuine",
        "confidence": float(probability),
        "features": features
    }

# User contribution endpoint
@app.post("/api/contribute")
async def contribute(contribution: dict, current_user: UserInDB = Depends(get_current_user)):
    freemium_service.add_contribution(current_user, contribution['type'])
    return {"message": "Contribution recorded"}

# User stats endpoint
@app.get("/api/user/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user_credentials)):
    firebase_uid = current_user['uid']
    user = User.find_by_firebase_uid(firebase_uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "tier": user.tier,
        "daily_scans": user.daily_scans,
        "contributions": user.contributions,
        "rewards": user.rewards
    }

# Admin routes
@app.get("/api/admin/users", response_model=List[UserSchema])
async def get_all_users(current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    users = user_service.get_all_users()
    return [UserSchema(**user.to_dict()) for user in users]

@app.get("/api/admin/stats")
async def get_admin_stats(current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return {
        "totalUsers": user_service.get_total_users(),
        "proUsers": user_service.get_pro_users(),
        "totalScans": freemium_service.get_total_scans(),
        "totalContributions": freemium_service.get_total_contributions()
    }

@app.get("/api/admin/user/{user_id}", response_model=UserSchema)
async def get_user_details(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema(**user.to_dict())

@app.put("/api/admin/user/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user_data: dict, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    updated_user = user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema(**updated_user.to_dict())

# Feature toggle endpoints
@app.get("/api/user/features")
async def get_user_features(current_user: UserInDB = Depends(get_current_user)):
    return feature_toggle.get_user_features(current_user)

@app.post("/api/user/unlock-feature")
async def unlock_feature(feature: str, current_user: UserInDB = Depends(get_current_user)):
    success = feature_toggle.unlock_feature(current_user, feature)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to unlock feature")
    return {"message": "Feature unlocked successfully"}

# Data collection endpoint
data_collector = DataCollector()

@app.post("/api/collect-profile")
async def collect_profile(profile_data: dict, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    platform = profile_data.get('platform')
    profile_url = profile_data.get('profile_url')
    
    if not platform or not profile_url:
        raise HTTPException(status_code=400, detail="Platform and profile_url are required")
    
    try:
        collected_data = data_collector.collect_profile(platform, profile_url)
        return {"message": "Profile collected successfully", "data": collected_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error collecting profile: {str(e)}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
