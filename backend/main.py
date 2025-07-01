"""
🌌 NOVA: The Writers' Conspiracy - Main FastAPI Application
A cosmic atelier where storytellers conspire with AI to birth entire universes
"""

import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from app.core.celery import celery_app

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - the ritual of awakening and slumber"""
    # Startup - Awakening the cosmic atelier
    logger.info("🌌 Awakening NOVA: The Writers' Conspiracy")
    
    # Create database tables - the neural graveyard where memories live
    from app.core.database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("🧠 Neural graveyard prepared - memories await")
    
    yield
    
    # Shutdown - the ritual of slumber
    logger.info("🌙 NOVA enters the realm of dreams")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application - the sacred vessel"""
    
    # CORS origins - the bridges between realms
    origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["http://localhost:3000"]
    
    app = FastAPI(
        title="🌌 NOVA: The Writers' Conspiracy API",
        description="A cosmic atelier where storytellers conspire with AI to birth entire universes. Four sacred roles, six divine agents, infinite possibilities.",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add middleware - the protective sigils
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware for production - the guardian of realms
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure appropriately for production
        )
    
    # Include API routes - the sacred paths
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check endpoint - the heartbeat of the conspiracy
    @app.get("/health")
    async def health_check():
        """Health check endpoint - the pulse of creation"""
        return {
            "status": "🌌 alive and conspiring",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "message": "The cosmic atelier hums with possibility"
        }
    
    # Root endpoint - the gateway to the conspiracy
    @app.get("/")
    async def root():
        """Root endpoint - the sacred threshold"""
        return {
            "message": "🌌 Welcome to NOVA: The Writers' Conspiracy",
            "version": "1.0.0",
            "description": "A cosmic atelier where storytellers conspire with AI",
            "docs": "/docs" if settings.DEBUG else None,
            "quote": "They said creation was lonely. They were wrong."
        }
    
    # Global exception handler - the guardian of errors
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler - when the ritual falters"""
        logger.error(
            "Unhandled exception in the cosmic atelier",
            exc_info=exc,
            path=request.url.path,
            method=request.method
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "detail": "The conspiracy encountered an unexpected twist",
                "type": "internal_error",
                "message": "Even the most divine systems sometimes stumble"
            }
        )
    
    return app


# Create the application instance - the vessel of creation
app = create_application()

# Export for Celery - the worker of dreams
__all__ = ["app", "celery_app"] 