"""API module initialization."""

from fastapi import APIRouter
from app.api.prices import router as prices_router
from app.api.alerts import router as alerts_router
from app.api.markets import router as markets_router

# Main API router
api_router = APIRouter(prefix="/api/v1")

# Include sub-routers
api_router.include_router(prices_router)
api_router.include_router(alerts_router)
api_router.include_router(markets_router)

__all__ = ["api_router"]
