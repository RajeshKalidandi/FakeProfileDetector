from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['fake_profile_detector']
profiles_collection = db['profiles']

class Profile:
    def __init__(self, platform, username, data, is_fake=None):
        self._id = ObjectId()
        self.platform = platform
        self.username = username
        self.data = data
        self.is_fake = is_fake
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.versions = []

    def save(self):
        profile_data = self.to_dict()
        profiles_collection.insert_one(profile_data)

    def update(self, new_data):
        old_version = {
            'data': self.data,
            'updated_at': self.updated_at
        }
        self.versions.append(old_version)
        self.data = new_data
        self.updated_at = datetime.utcnow()
        profiles_collection.update_one({'_id': self._id}, {'$set': self.to_dict()})

    def to_dict(self):
        return {
            '_id': self._id,
            'platform': self.platform,
            'username': self.username,
            'data': self.data,
            'is_fake': self.is_fake,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'versions': self.versions
        }

    @staticmethod
    def find_by_username(platform, username):
        profile_data = profiles_collection.find_one({'platform': platform, 'username': username})
        if profile_data:
            profile = Profile(profile_data['platform'], profile_data['username'], profile_data['data'], profile_data['is_fake'])
            profile._id = profile_data['_id']
            profile.created_at = profile_data['created_at']
            profile.updated_at = profile_data['updated_at']
            profile.versions = profile_data['versions']
            return profile
        return None
