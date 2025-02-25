class InsCodeError(Exception):
    """Base exception for InsCode AI."""
    pass

class APIError(InsCodeError):
    """Raised when API request fails."""
    pass

class ValidationError(InsCodeError):
    """Raised when input validation fails."""
    pass

class ModelNotFoundError(InsCodeError):
    """Raised when specified model is not available."""
    pass 