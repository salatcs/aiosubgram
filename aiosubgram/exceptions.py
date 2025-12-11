class SubgramError(Exception):
    """Base class for exceptions in this module."""
    pass

class APIError(SubgramError):
    """Exception raised for API errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")

class NetworkError(SubgramError):
    """Exception raised for network errors."""
    pass

class AuthError(SubgramError):
    """Exception raised for authentication errors."""
    def __init__(self):
        super().__init__("API keys are not provided or invalid.")