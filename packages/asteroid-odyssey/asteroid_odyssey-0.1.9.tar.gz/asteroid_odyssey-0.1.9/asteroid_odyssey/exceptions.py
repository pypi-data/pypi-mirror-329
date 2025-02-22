"""Custom exceptions for the Asteroid Odyssey SDK."""

from typing import Optional


class AsteroidOdysseyError(Exception):
    """Base exception for all Asteroid Odyssey errors."""
    pass

class ApiError(AsteroidOdysseyError):
    """Raised when an API error occurs."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
