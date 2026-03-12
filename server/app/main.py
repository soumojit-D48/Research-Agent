
import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.exceptions import BaseAPIException
from app.core.error_handlers import (
    base_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)
from app.api.routes import research, conversations

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# -------------------------------------------------------------------
# FastAPI Application
# -------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Exception Handlers
# -------------------------------------------------------------------

app.add_exception_handler(BaseAPIException, base_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# -------------------------------------------------------------------
# Routers
# -------------------------------------------------------------------

app.include_router(
    research.router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    conversations.router,
    prefix=settings.API_PREFIX,
)

# -------------------------------------------------------------------
# Health & Root Endpoints
# -------------------------------------------------------------------

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
    }















# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.exceptions import RequestValidationError
# from sqlalchemy.exc import SQLAlchemyError

# from app.api.routes import research
# from app.core.config import settings
# from app.core.exceptions import BaseAPIException
# from app.core.error_handlers import (
#     base_exception_handler,
#     validation_exception_handler,
#     sqlalchemy_exception_handler,
#     generic_exception_handler
# )
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

# app = FastAPI(
#     title="AI Research Agent API",
#     version="2.0.0",
#     debug=settings.DEBUG
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Register exception handlers
# app.add_exception_handler(BaseAPIException, base_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
# app.add_exception_handler(Exception, generic_exception_handler)

# # Include routers
# app.include_router(research.router, prefix=settings.API_PREFIX)

# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "version": "2.0.0",
#         "environment": settings.APP_ENV
#     }

# @app.get("/")
# async def root():
#     return {
#         "message": "AI Research Agent API",
#         "docs": "/docs",
#         "health": "/health"
#     }
    