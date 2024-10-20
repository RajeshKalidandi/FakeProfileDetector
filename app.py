from fastapi import FastAPI, Depends, HTTPException, Request, Body, File, UploadFile, Form, BackgroundTasks, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from backend.models.user import User
from schemas import UserCreate, UserLogin, UserSchema, UserInDB, ProfileSubmission, BatchProfileSubmission, FeedbackSubmission
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
import pickle
import hashlib
from redis import Redis
from pymongo import MongoClient
from datetime import datetime
from ml_models.continuous_learning import continuous_learner
import threading
import asyncio
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from typing import Optional
import redis
from services.logging_service import logging_service
from services.monitoring_service import monitoring_service
from apscheduler.schedulers.background import BackgroundScheduler
from background_jobs import start_background_jobs

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

# Setup rate limiting
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = redis.from_url(redis_url)
FastAPILimiter.init(redis)

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User model
class User(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Password hashing functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Authentication routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Apply rate limiting to all routes
@app.middleware("http")
async def add_rate_limit_to_all_routes(request: Request, call_next):
    limiter = RateLimiter(times=100, hours=1)  # 100 requests per hour
    await limiter(request)
    response = await call_next(request)
    return response

async def get_current_user_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Initialize Redis client
redis_client = Redis(host='localhost', port=6379, db=0)

# Initialize MongoDB client
mongo_client = MongoClient(os.getenv('MONGODB_URI'))
db = mongo_client['fake_profile_detector']
users_collection = db['users']
profiles_collection = db['profiles']
analysis_results_collection = db['analysis_results']
feedback_reports_collection = db['feedback_reports']
model_versions_collection = db['model_versions']
feature_importance_collection = db['feature_importance']

# Helper function to generate a unique key for a profile
def generate_profile_key(profile_data):
    return hashlib.md5(json.dumps(profile_data, sort_keys=True).encode()).hexdigest()

# Background task to update cache
def update_cache(profile_key, analysis_result):
    redis_client.setex(profile_key, 3600, pickle.dumps(analysis_result))  # Cache for 1 hour

# Add this function to initialize the analyses collection
def init_analyses_collection():
    if 'analyses' not in db.list_collection_names():
        db.create_collection('analyses')
        analyses_collection.create_index([('user_id', 1), ('created_at', -1)])
        print("Analyses collection created and indexed.")

# Call this function when the app starts
init_analyses_collection()

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
    current_user: User = Depends(get_current_active_user),
    limiter: RateLimiter = Depends(RateLimiter(times=10, minutes=1))  # 10 requests per minute
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
    
    # Add network-related data to profile_data
    profile_data['id'] = str(current_user.id)
    profile_data['followers_count'] = current_user.followers_count
    profile_data['following_count'] = current_user.following_count
    profile_data['connections'] = current_user.connections

    # Add temporal data to profile_data
    profile_data['user'] = current_user

    features = extract_features(profile_data)
    model = continuous_learner.current_model
    
    feature_list = [features[f] for f in model.feature_names_]
    
    prediction = model.predict([feature_list])[0]
    probability = model.predict_proba([feature_list])[0][1]

    analysis_result = {
        "user_id": str(current_user.id),
        "profile_url": profile_data.get('profile_url', ''),
        "result": "fake" if prediction == 1 else "genuine",
        "confidence": float(probability),
        "features": features,
        "created_at": datetime.utcnow()
    }

    # Log the prediction
    logging_service.log_prediction(
        analysis_result["user_id"],
        analysis_result["profile_url"],
        analysis_result["result"],
        analysis_result["confidence"]
    )

    # Store the analysis result in the analyses collection
    analyses_collection.insert_one(analysis_result)

    freemium_service.increment_scan_count(current_user)
    
    # Remove the temporary image files
    for temp_path in temp_image_paths:
        os.remove(temp_path)
    
    return {
        "result": analysis_result["result"],
        "confidence": analysis_result["confidence"],
        "features": analysis_result["features"]
    }

# Asynchronous background task for profile analysis
async def analyze_profile_background(profile_data: dict, current_user: UserInDB):
    features = extract_features(profile_data)
    model = continuous_learner.current_model
    
    feature_list = [features[f] for f in model.feature_names_]
    
    prediction = model.predict([feature_list])[0]
    probability = model.predict_proba([feature_list])[0][1]
    
    analysis_result = {
        "user_id": str(current_user.id),
        "profile_url": profile_data.get('profile_url', ''),
        "result": "fake" if prediction == 1 else "genuine",
        "confidence": float(probability),
        "features": features,
        "created_at": datetime.utcnow()
    }

    # Store the analysis result in the analyses collection
    analyses_collection.insert_one(analysis_result)
    
    # Update cache
    profile_key = generate_profile_key(profile_data)
    redis_client.setex(profile_key, 3600, pickle.dumps(analysis_result))  # Cache for 1 hour
    
    freemium_service.increment_scan_count(current_user)

@app.post("/api/analyze/profile/realtime")
async def analyze_profile_realtime(
    profile_data: dict = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: UserInDB = Depends(get_current_user)
):
    if not freemium_service.check_scan_limit(current_user):
        raise HTTPException(status_code=403, detail="Daily scan limit reached")
    
    profile_key = generate_profile_key(profile_data)
    
    # Check if the analysis result is in cache
    cached_result = redis_client.get(profile_key)
    if cached_result:
        return pickle.loads(cached_result)
    
    # Start asynchronous analysis
    background_tasks.add_task(analyze_profile_background, profile_data, current_user)
    
    return {"message": "Analysis started. Results will be available shortly."}

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
    
    # Update network features before returning stats
    user_service.update_user_network_features(user)
    
    return user_service.get_user_stats(user)

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

# Recent analyses endpoint
@app.get("/api/recent-analyses")
async def get_recent_analyses(current_user: UserInDB = Depends(get_current_user)):
    # Fetch the 5 most recent analyses for the current user
    recent_analyses = await user_service.get_recent_analyses(current_user.id, limit=5)
    return recent_analyses

@app.post("/api/feedback")
async def submit_feedback(analysis_id: str, feedback: str, current_user: UserInDB = Depends(get_current_user)):
    continuous_learner.collect_feedback(analysis_id, feedback)
    return {"message": "Feedback submitted successfully"}

@app.post("/api/admin/retrain")
async def retrain_model(current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    continuous_learner.retrain_model()
    return {"message": "Model retraining initiated"}

@app.post("/api/admin/ab-test")
async def start_ab_test(test_duration_hours: int, current_user: UserInDB = Depends(get_current_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Implement A/B testing logic here
    # This could involve setting a flag in the database to use the new model for a subset of users
    # and comparing performance metrics after the test duration
    
    return {"message": f"A/B test started for {test_duration_hours} hours"}

@app.get("/api/admin/monitoring/performance")
async def get_system_performance(days: int = 7, current_user: User = Depends(get_current_active_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return monitoring_service.get_system_performance(days)

@app.get("/api/admin/monitoring/daily-analysis")
async def get_daily_analysis_count(days: int = 30, current_user: User = Depends(get_current_active_user)):
    if not user_service.is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return monitoring_service.get_daily_analysis_count(days)

# API versioning
v1_router = APIRouter(prefix="/api/v1")

# User registration and authentication
@v1_router.post("/auth/register", response_model=UserSchema)
async def register(user_data: UserCreate):
    try:
        user = auth_service.register_user(user_data.username, user_data.email, user_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user_dict = user.to_dict()
        user_dict['id'] = str(user_dict['_id'])
        del user_dict['_id']
        return UserSchema(**user_dict)
    except Exception as e:
        logging_service.log_error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@v1_router.post("/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.login_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    access_token = User.generate_token(user['id'])
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# Profile submission for analysis
@v1_router.post("/analyze/profile")
async def analyze_profile(
    profile_data: ProfileSubmission,
    current_user: UserInDB = Depends(get_current_user),
    limiter: RateLimiter = Depends(RateLimiter(times=10, minutes=1))
):
    if not freemium_service.check_scan_limit(current_user):
        raise HTTPException(status_code=403, detail="Daily scan limit reached")
    
    features = extract_features(profile_data.dict())
    model = continuous_learner.current_model
    
    feature_list = [features[f] for f in model.feature_names_]
    
    prediction = model.predict([feature_list])[0]
    probability = model.predict_proba([feature_list])[0][1]

    analysis_result = {
        "user_id": str(current_user.id),
        "profile_url": profile_data.profile_url,
        "result": "fake" if prediction == 1 else "genuine",
        "confidence": float(probability),
        "features": features,
        "created_at": datetime.utcnow()
    }

    analyses_collection.insert_one(analysis_result)
    logging_service.log_prediction(analysis_result["user_id"], analysis_result["profile_url"], analysis_result["result"], analysis_result["confidence"])
    freemium_service.increment_scan_count(current_user)
    
    return analysis_result

# Batch profile analysis
@v1_router.post("/analyze/batch")
async def analyze_batch_profiles(
    batch_data: BatchProfileSubmission,
    current_user: UserInDB = Depends(get_current_user),
    limiter: RateLimiter = Depends(RateLimiter(times=5, minutes=10))
):
    if not freemium_service.check_batch_scan_limit(current_user, len(batch_data.profiles)):
        raise HTTPException(status_code=403, detail="Batch scan limit reached")
    
    results = []
    for profile in batch_data.profiles:
        features = extract_features(profile.dict())
        model = continuous_learner.current_model
        
        feature_list = [features[f] for f in model.feature_names_]
        
        prediction = model.predict([feature_list])[0]
        probability = model.predict_proba([feature_list])[0][1]

        analysis_result = {
            "user_id": str(current_user.id),
            "profile_url": profile.profile_url,
            "result": "fake" if prediction == 1 else "genuine",
            "confidence": float(probability),
            "features": features,
            "created_at": datetime.utcnow()
        }

        analyses_collection.insert_one(analysis_result)
        logging_service.log_prediction(analysis_result["user_id"], analysis_result["profile_url"], analysis_result["result"], analysis_result["confidence"])
        results.append(analysis_result)
    
    freemium_service.increment_batch_scan_count(current_user, len(batch_data.profiles))
    
    return results

# Retrieving analysis results
@v1_router.get("/analysis/results")
async def get_analysis_results(
    current_user: UserInDB = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    results = list(analyses_collection.find(
        {"user_id": str(current_user.id)},
        {"_id": 0}
    ).sort("created_at", -1).skip(offset).limit(limit))
    
    return results

# Submitting feedback on analysis results
@v1_router.post("/analysis/feedback")
async def submit_feedback(
    feedback: FeedbackSubmission,
    current_user: UserInDB = Depends(get_current_user)
):
    analysis = analyses_collection.find_one({"_id": ObjectId(feedback.analysis_id)})
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis["user_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to submit feedback for this analysis")
    
    feedback_data = {
        "user_id": str(current_user.id),
        "analysis_id": feedback.analysis_id,
        "feedback": feedback.feedback,
        "created_at": datetime.utcnow()
    }
    
    feedback_collection.insert_one(feedback_data)
    continuous_learner.collect_feedback(feedback.analysis_id, feedback.feedback)
    
    return {"message": "Feedback submitted successfully"}

# CRUD operations for Profiles
@app.post("/api/profiles")
async def create_profile(profile: ProfileSubmission, current_user: UserInDB = Depends(get_current_user)):
    profile_data = profile.dict()
    profile_data['user_id'] = ObjectId(current_user.id)
    profile_data['created_at'] = datetime.utcnow()
    profile_data['last_updated'] = datetime.utcnow()
    result = profiles_collection.insert_one(profile_data)
    return {"id": str(result.inserted_id)}

@app.get("/api/profiles/{profile_id}")
async def get_profile(profile_id: str, current_user: UserInDB = Depends(get_current_user)):
    profile = profiles_collection.find_one({"_id": ObjectId(profile_id), "user_id": ObjectId(current_user.id)})
    if profile:
        profile['_id'] = str(profile['_id'])
        return profile
    raise HTTPException(status_code=404, detail="Profile not found")

# CRUD operations for AnalysisResults
@app.post("/api/analysis_results")
async def create_analysis_result(result: AnalysisResultSubmission, current_user: UserInDB = Depends(get_current_user)):
    result_data = result.dict()
    result_data['user_id'] = ObjectId(current_user.id)
    result_data['created_at'] = datetime.utcnow()
    result = analysis_results_collection.insert_one(result_data)
    return {"id": str(result.inserted_id)}

@app.get("/api/analysis_results/{result_id}")
async def get_analysis_result(result_id: str, current_user: UserInDB = Depends(get_current_user)):
    result = analysis_results_collection.find_one({"_id": ObjectId(result_id), "user_id": ObjectId(current_user.id)})
    if result:
        result['_id'] = str(result['_id'])
        return result
    raise HTTPException(status_code=404, detail="Analysis result not found")

# CRUD operations for FeedbackReports
@app.post("/api/feedback_reports")
async def create_feedback_report(feedback: FeedbackReportSubmission, current_user: UserInDB = Depends(get_current_user)):
    feedback_data = feedback.dict()
    feedback_data['user_id'] = ObjectId(current_user.id)
    feedback_data['created_at'] = datetime.utcnow()
    result = feedback_reports_collection.insert_one(feedback_data)
    return {"id": str(result.inserted_id)}

@app.get("/api/feedback_reports/{report_id}")
async def get_feedback_report(report_id: str, current_user: UserInDB = Depends(get_current_user)):
    report = feedback_reports_collection.find_one({"_id": ObjectId(report_id), "user_id": ObjectId(current_user.id)})
    if report:
        report['_id'] = str(report['_id'])
        return report
    raise HTTPException(status_code=404, detail="Feedback report not found")

# Include the v1 router in the main app
app.include_router(v1_router)

@app.on_event("startup")
async def startup_event():
    start_background_jobs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Add this at the end of the file
retraining_thread = threading.Thread(target=continuous_learner.schedule_retraining)
retraining_thread.start()

scheduler = BackgroundScheduler()
scheduler.add_job(monitoring_service.check_for_anomalies, 'interval', hours=24)
scheduler.start()
