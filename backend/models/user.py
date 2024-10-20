from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from typing import Dict, List
from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from services.encryption_service import encryption_service

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['fake_profile_detector']
users_collection = db['users']

JWT_SECRET = os.getenv('JWT_SECRET')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    tier = Column(String, index=True)
    daily_scans = Column(Integer)
    last_reset = Column(DateTime)
    contributions = Column(JSON)
    rewards = Column(JSON)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    connections = Column(JSON)
    follower_following_ratio = Column(Float)
    degree_centrality = Column(Float)
    betweenness_centrality = Column(Float)
    closeness_centrality = Column(Float)
    clustering_coefficient = Column(Float)
    network_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_login = Column(DateTime)
    post_count = Column(Integer, default=0)
    activity_times = Column(JSON)

    # Create composite index for faster queries
    __table_args__ = (
        Index('idx_tier_daily_scans', 'tier', 'daily_scans'),
    )

    def __init__(self, username: str, email: str, password_hash: str, tier: str = 'free', daily_scans: int = 0, last_reset: datetime = datetime.utcnow(), _id: ObjectId = None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.tier = tier
        self.daily_scans = daily_scans
        self.last_reset = last_reset
        self.contributions = {
            'verifiedProfiles': 0,
            'validReports': 0,
            'feedbackCount': 0,
            'total_points': 0
        }
        self.rewards = []
        self.followers_count = 0
        self.following_count = 0
        self.connections = []
        self.follower_following_ratio = 0.0
        self.degree_centrality = 0.0
        self.betweenness_centrality = 0.0
        self.closeness_centrality = 0.0
        self.clustering_coefficient = 0.0
        self.network_score = 0.0
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.post_count = 0
        self.activity_times = []

    @property
    def id(self):
        return str(self._id)

    @property
    def email(self):
        return encryption_service.decrypt(self._email)
    
    @email.setter
    def email(self, value):
        self._email = encryption_service.encrypt(value)

    def save(self):
        if not self._id:
            result = users_collection.insert_one(self.to_dict())
            self._id = result.inserted_id
        else:
            users_collection.update_one({'_id': self._id}, {'$set': self.to_dict()})

    def to_dict(self):
        return {
            "_id": str(self._id),  # Convert ObjectId to string
            "username": self.username,
            "email": self.email,
            "tier": self.tier,
            "daily_scans": self.daily_scans,
            "last_reset": self.last_reset,
            "contributions": self.contributions,
            "rewards": self.rewards,
            "followers_count": self.followers_count,
            "following_count": self.following_count,
            "connections": self.connections,
            "follower_following_ratio": self.follower_following_ratio,
            "degree_centrality": self.degree_centrality,
            "betweenness_centrality": self.betweenness_centrality,
            "closeness_centrality": self.closeness_centrality,
            "clustering_coefficient": self.clustering_coefficient,
            "network_score": self.network_score,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "post_count": self.post_count,
            "activity_times": self.activity_times,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            tier=data.get('tier', 'free'),
            daily_scans=data.get('daily_scans', 0),
            last_reset=data.get('last_reset', datetime.utcnow()),
            _id=data.get('_id')
        )
        user.contributions = data.get('contributions', user.contributions)
        user.rewards = data.get('rewards', user.rewards)
        return user

    @staticmethod
    def find_by_id(user_id: str) -> 'User':
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        return User.from_dict(user_data) if user_data else None

    @staticmethod
    def find_by_email(email: str) -> 'User':
        user_data = users_collection.find_one({'email': email})
        return User.from_dict(user_data) if user_data else None

    @staticmethod
    def find_by_username(username: str) -> 'User':
        user_data = users_collection.find_one({'username': username})
        return User.from_dict(user_data) if user_data else None

    def generate_token(self) -> str:
        payload = {
            'user_id': str(self._id),
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    @staticmethod
    def verify_token(token: str) -> 'User':
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return User.find_by_id(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def update_daily_scans(self):
        today = datetime.utcnow().date()
        if self.last_reset.date() < today:
            self.daily_scans = 0
            self.last_reset = datetime.utcnow()
        self.daily_scans += 1
        self.save()

    def add_contribution(self, contribution_type: str):
        if contribution_type in self.contributions:
            self.contributions[contribution_type] += 1
            self.contributions['total_points'] += 1
            self.save()

    @staticmethod
    def get_all_users() -> List['User']:
        return [User.from_dict(user_data) for user_data in users_collection.find()]

    @staticmethod
    def get_total_users() -> int:
        return users_collection.count_documents({})

    @staticmethod
    def get_pro_users() -> int:
        return users_collection.count_documents({'tier': 'pro'})

    @staticmethod
    def get_total_scans() -> int:
        return sum(user['daily_scans'] for user in users_collection.find())

    @staticmethod
    def get_total_contributions() -> int:
        return sum(sum(user['contributions'].values()) for user in users_collection.find())

    def update_login(self):
        self.last_login = datetime.utcnow()
        self.save()

    def add_post(self):
        self.post_count += 1
        self.activity_times.append(datetime.utcnow().isoformat())
        self.save()

    def get_account_age(self):
        return (datetime.utcnow() - self.created_at).days

    def get_posting_frequency(self):
        account_age_days = self.get_account_age()
        return self.post_count / account_age_days if account_age_days > 0 else 0

    def get_activity_pattern(self):
        hour_counts = [0] * 24
        for activity_time in self.activity_times:
            hour = datetime.fromisoformat(activity_time).hour
            hour_counts[hour] += 1
        return hour_counts

# Create indexes for MongoDB
users_collection.create_index([("email", ASCENDING)], unique=True)
users_collection.create_index([("username", ASCENDING)])
users_collection.create_index([("tier", ASCENDING)])
users_collection.create_index([("created_at", ASCENDING)])
