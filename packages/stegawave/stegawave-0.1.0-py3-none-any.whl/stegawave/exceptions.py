class StegawaveError(Exception):
    """Base exception for Stegawave API errors."""
    pass

class AuthenticationError(StegawaveError):
    """Raised when there are authentication issues."""
    pass