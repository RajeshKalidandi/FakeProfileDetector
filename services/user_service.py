from backend.models.user import User
from typing import List
from ml_models.network_feature_extraction import extract_network_features
from ml_models.temporal_feature_extraction import extract_temporal_features
from pymongo import MongoClient
from redis import Redis
import pickle
import json
from passlib.context import CryptContext

# Initialize Redis client
redis_client = Redis(host='localhost', port=6379, db=1)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_admin(user: User) -> bool:
    # Implement admin check logic
    return user.email in ['admin@example.com']  # Replace with your admin emails

def get_all_users() -> List[User]:
    return User.get_all_users()

def get_total_users() -> int:
    return User.get_total_users()

def get_pro_users() -> int:
    return User.get_pro_users()

def get_user_by_id(user_id: str) -> User:
    return User.find_by_id(user_id)

def update_user(user_id: str, user_data: dict) -> User:
    user = User.find_by_id(user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()
    return user

def get_user_from_token(token: str) -> User:
    # Implement token validation and user retrieval
    # This is a placeholder implementation
    return User.find_by_email(token)  # Replace with proper token validation

def update_user_network_features(user: User):
    network_features = extract_network_features(
        user.id,
        user.followers_count,
        user.following_count,
        user.connections
    )
    
    user.follower_following_ratio = network_features['follower_following_ratio']
    user.degree_centrality = network_features['degree_centrality']
    user.betweenness_centrality = network_features['betweenness_centrality']
    user.closeness_centrality = network_features['closeness_centrality']
    user.clustering_coefficient = network_features['clustering_coefficient']
    
    # Calculate a simple network score (you can adjust this calculation as needed)
    user.network_score = (
        user.follower_following_ratio +
        user.degree_centrality +
        user.betweenness_centrality +
        user.closeness_centrality +
        user.clustering_coefficient
    ) / 5

    user.save()

def get_user_stats(user: User):
    cache_key = f"user_stats:{user.id}"
    cached_stats = redis_client.get(cache_key)
    
    if cached_stats:
        return json.loads(cached_stats)
    
    temporal_features = extract_temporal_features(user)
    stats = {
        "tier": user.tier,
        "daily_scans": user.daily_scans,
        "contributions": user.contributions,
        "rewards": user.rewards,
        "network_score": user.network_score,
        "follower_following_ratio": user.follower_following_ratio,
        "degree_centrality": user.degree_centrality,
        "betweenness_centrality": user.betweenness_centrality,
        "closeness_centrality": user.closeness_centrality,
        "clustering_coefficient": user.clustering_coefficient,
        "account_age": temporal_features['account_age'],
        "posting_frequency": temporal_features['posting_frequency'],
        "activity_variance": temporal_features['activity_variance'],
        "night_day_ratio": temporal_features['night_day_ratio'],
    }
    
    # Cache the stats for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(stats))
    
    return stats

async def get_recent_analyses(user_id: str, limit: int = 5) -> List[dict]:
    cache_key = f"recent_analyses:{user_id}"
    cached_analyses = redis_client.get(cache_key)
    
    if cached_analyses:
        return pickle.loads(cached_analyses)
    
    analyses = list(db.analyses.find({"user_id": user_id}).sort("created_at", -1).limit(limit))
    
    result = [
        {
            "profile_url": analysis["profile_url"],
            "result": analysis["result"],
            "confidence": analysis["confidence"],
            "created_at": analysis["created_at"]
        }
        for analysis in analyses
    ]
    
    # Cache the results for 1 minute
    redis_client.setex(cache_key, 60, pickle.dumps(result))
    
    return result

def create_user(username: str, email: str, password: str) -> User:
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    user.save()
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
