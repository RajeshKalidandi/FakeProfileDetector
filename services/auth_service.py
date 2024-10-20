from backend.models.user import User
from werkzeug.security import generate_password_hash
from .logger import auth_logger

def register_user(username: str, email: str, password: str) -> User:
    auth_logger.info(f"Attempting to register user: {email}")
    if User.find_by_email(email):
        auth_logger.warning(f"Registration failed: Email already exists: {email}")
        return None
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    new_user.save()
    auth_logger.info(f"User registered successfully: {email}")
    return new_user

def login_user(email, password):
    user = User.find_by_email(email)
    if user and bcrypt.verify(password, user.password_hash):
        return user.to_dict()  # Return a dictionary representation
    return None
