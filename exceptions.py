class AppError(Exception):
    """Base error class for application exceptions"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(AppError):
    """Raised when authentication fails"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message, status_code=401)

class AuthorizationError(AppError):
    """Raised when user is not authorized to perform an action"""
    def __init__(self, message="You are not authorized to perform this action"):
        super().__init__(message, status_code=403)

class ResourceNotFoundError(AppError):
    """Raised when a requested resource is not found"""
    def __init__(self, message="Requested resource not found"):
        super().__init__(message, status_code=404)
