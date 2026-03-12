
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
import traceback
from app.core.exceptions import BaseAPIException

logger = logging.getLogger(__name__)

async def base_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions"""
    logger.error(
        f"API Exception: {exc.error_code} - {exc.detail}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_code": exc.error_code
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "path": request.url.path
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": exc.errors()
            }
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Database operation failed",
                "path": request.url.path
            }
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={"traceback": traceback.format_exc()}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "path": request.url.path
            }
        }
    )