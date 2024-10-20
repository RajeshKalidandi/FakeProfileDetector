from backend.models.user import User
from typing import List

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
