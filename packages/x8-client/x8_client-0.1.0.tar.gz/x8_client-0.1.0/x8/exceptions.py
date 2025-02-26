"""Custom exceptions for the x8 package."""

class APIError(Exception):
    """Base exception for API related errors."""
    pass

class VideoProcessingError(APIError):
    """Raised when video processing fails."""
    pass
