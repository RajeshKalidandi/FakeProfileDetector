from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['fake_profile_detector']
users_collection = db['users']

JWT_SECRET = os.getenv('JWT_SECRET')

class User:
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

    @property
    def id(self):
        return str(self._id)

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
            "password_hash": self.password_hash
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
