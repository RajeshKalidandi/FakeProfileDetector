from fastapi import FastAPI, Depends, HTTPException, Request
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
    user_dict = user.__dict__
    user_dict['id'] = str(user_dict.pop('_id'))  # Convert ObjectId to string
    return UserInDB(**user_dict)

async def get_current_user_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# New authentication endpoints
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

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.login_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    access_token = User.generate_token(user['id'])
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.get("/api/auth/me", response_model=UserSchema)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    return UserSchema(**current_user.__dict__)

# Existing routes
@app.post("/api/analyze/profile")
async def analyze_profile(profile_data: dict, current_user: UserInDB = Depends(get_current_user)):
    if not freemium_service.check_scan_limit(current_user):
        raise HTTPException(status_code=403, detail="Daily scan limit reached")
    
    # Perform analysis
    freemium_service.increment_scan_count(current_user)
    return {"result": "Analysis completed"}

@app.post("/api/contribute")
async def contribute(contribution: dict, current_user: UserInDB = Depends(get_current_user)):
    freemium_service.add_contribution(current_user, contribution['type'])
    return {"message": "Contribution recorded"}

@app.get("/api/user/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user_credentials)):
    # Use the Firebase UID from the decoded token
    firebase_uid = current_user['uid']
    # Fetch user data from your database using the Firebase UID
    user = User.find_by_firebase_uid(firebase_uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "tier": user.tier,
        "daily_scans": user.daily_scans,
        "contributions": user.contributions,
        "rewards": user.rewards
    }

# New admin routes
@app.get("/api/admin/users", response_model=List[UserSchema])
async def get_all_users(current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    users = user_service.get_all_users()
    return [UserSchema(**user.__dict__) for user in users]

@app.get("/api/admin/stats")
async def get_admin_stats(current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    total_users = user_service.get_total_users()
    pro_users = user_service.get_pro_users()
    total_scans = freemium_service.get_total_scans()
    total_contributions = freemium_service.get_total_contributions()
    
    return {
        "totalUsers": total_users,
        "proUsers": pro_users,
        "totalScans": total_scans,
        "totalContributions": total_contributions
    }

@app.get("/api/admin/user/{user_id}", response_model=UserSchema)
async def get_user_details(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema(**user.__dict__)

@app.put("/api/admin/user/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user_data: dict, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    updated_user = user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema(**updated_user.__dict__)

@app.get("/api/user/features")
async def get_user_features(current_user: UserInDB = Depends(get_current_user)):
    return feature_toggle.get_user_features(current_user)

@app.post("/api/user/unlock-feature")
async def unlock_feature(feature: str, current_user: UserInDB = Depends(get_current_user)):
    success = feature_toggle.unlock_feature(current_user, feature)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to unlock feature")
    return {"message": "Feature unlocked successfully"}

@app.get("/test-db")
async def test_db():
    try:
        # Create a test user
        test_user = User("testuser", "test@example.com", "password_hash")
        test_user.save()
        
        # Attempt to fetch the test user
        fetched_user = User.find_by_email("test@example.com")
        if fetched_user:
            return {"message": "In-memory storage is working", "user": fetched_user.username}
        else:
            return {"message": "Failed to retrieve test user"}
    except Exception as e:
        return {"message": "Test failed", "error": str(e), "traceback": traceback.format_exc()}

@app.get("/api/protected")
async def protected_route(current_user: dict = Depends(get_current_user_credentials)):
    return {"message": "This is a protected route", "user": current_user}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
