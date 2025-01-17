class TimestoneAPIError(Exception):
    """Base exception for Timestone API errors"""
    pass

class ValidationError(TimestoneAPIError):
    """Raised when input validation fails"""
    pass

class AuthenticationError(TimestoneAPIError):
    """Raised when authentication fails"""
    pass

class SchedulingError(TimestoneAPIError):
    """Raised when message scheduling fails"""
    pass