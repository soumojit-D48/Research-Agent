
from fastapi import HTTPException, status
from typing import Any, Optional

class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code

class DatabaseException(BaseAPIException):
    """Database operation errors"""
    def __init__(self, detail: str, error_code: str = "DB_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )

class SearchException(BaseAPIException):
    """Web search errors"""
    def __init__(self, detail: str, error_code: str = "SEARCH_ERROR"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code=error_code
        )

class AgentException(BaseAPIException):
    """Agent execution errors"""
    def __init__(self, detail: str, error_code: str = "AGENT_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )

class ValidationException(BaseAPIException):
    """Input validation errors"""
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code
        )

class RateLimitException(BaseAPIException):
    """Rate limit exceeded"""
    def __init__(self, detail: str = "Rate limit exceeded", error_code: str = "RATE_LIMIT"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code=error_code
        )

class ResourceNotFoundException(BaseAPIException):
    """Resource not found"""
    def __init__(self, detail: str, error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code
        )

