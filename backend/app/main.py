"""
BazaarSetu Backend - Main Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import get_settings
from app.core.database import init_db
from app.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting BazaarSetu API...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down BazaarSetu API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    **BazaarSetu API** - Live Vegetable Prices from AP & Telangana
    
    ## Features
    
    - **Live Prices**: Get today's vegetable prices from various mandis
    - **Price Trends**: Track price history over days, weeks, or months
    - **Market Comparison**: Compare prices across different markets
    - **Price Alerts**: Set alerts for when prices hit your target
    - **Multi-language**: Supports English, Telugu, and Hindi
    
    ## Data Sources
    
    - data.gov.in (Agmarknet)
    - eNAM (Electronic National Agriculture Market)
    """,
    version=settings.version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - allow Flutter app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "healthy",
        "message": "Welcome to BazaarSetu API! Visit /docs for API documentation."
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.version
    }
