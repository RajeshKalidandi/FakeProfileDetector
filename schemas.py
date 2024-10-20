from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserContributions(BaseModel):
    verifiedProfiles: int = 0
    validReports: int = 0
    feedbackCount: int = 0
    total_points: int = 0

class UserReward(BaseModel):
    type: str
    granted_at: datetime
    expires_at: datetime
    status: str

class UserSchema(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    tier: str = 'free'
    daily_scans: int = 0
    last_reset: datetime
    contributions: UserContributions = UserContributions()
    rewards: List[UserReward] = []

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class UserInDB(UserSchema):
    password_hash: str
