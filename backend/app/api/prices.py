"""
BazaarSetu Backend - Price API Routes
"""

from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import PriceService, price_data_service
from app.schemas import (
    PriceWithDetails,
    PriceTrend,
    MarketComparison,
    CommodityResponse
)

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/today", response_model=List[PriceWithDetails])
async def get_today_prices(
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    commodity_id: Optional[int] = Query(None, description="Filter by commodity ID"),
    market_id: Optional[int] = Query(None, description="Filter by market ID"),
    category: Optional[str] = Query(None, description="Filter by category (vegetable, poultry, leafy, etc.)"),
    sort_by: Optional[str] = Query("name", description="Sort by: name, price, change"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc, desc"),
    date_from: Optional[date] = Query(None, description="Start date for price range"),
    date_to: Optional[date] = Query(None, description="End date for price range"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=200, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get today's vegetable prices.
    
    Returns prices with optional filtering by state, commodity, market, or category.
    Supports sorting by name, price, or price change.
    Includes price change percentage compared to yesterday.
    """
    service = PriceService(db)
    return await service.get_today_prices(
        state_id=state_id,
        commodity_id=commodity_id,
        market_id=market_id,
        category=category,
        sort_by=sort_by,
        sort_order=sort_order,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size
    )


@router.get("/trend/{commodity_id}", response_model=PriceTrend)
async def get_price_trend(
    commodity_id: int,
    market_id: Optional[int] = Query(None, description="Specific market (optional)"),
    days: int = Query(30, ge=7, le=365, description="Number of days for trend"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get price trend for a commodity.
    
    Returns historical prices with average, min, max, and percentage changes.
    If no market specified, returns average across all markets.
    """
    service = PriceService(db)
    try:
        return await service.get_price_trend(
            commodity_id=commodity_id,
            market_id=market_id,
            days=days
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/compare/{commodity_id}", response_model=MarketComparison)
async def compare_markets(
    commodity_id: int,
    price_date: Optional[date] = Query(None, description="Date to compare (default: today)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Compare prices across markets for a commodity.
    
    Returns prices from all available markets, sorted by modal price.
    Helps find the cheapest market for a vegetable.
    """
    service = PriceService(db)
    try:
        return await service.compare_markets(
            commodity_id=commodity_id,
            target_date=price_date
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/search", response_model=List[CommodityResponse])
async def search_commodities(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=50, description="Max results"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for commodities by name.
    
    Supports search in English, Telugu, and Hindi names.
    """
    service = PriceService(db)
    commodities = await service.search_commodities(query=q, limit=limit)
    return [CommodityResponse.model_validate(c) for c in commodities]


@router.get("/fetch-live")
async def fetch_live_prices():
    """
    Trigger a manual fetch of live prices from data.gov.in.
    
    This endpoint is for testing/admin purposes.
    In production, prices are fetched automatically via scheduled tasks.
    """
    try:
        records = await price_data_service.fetch_all_prices()
        summary = await price_data_service.get_price_summary(records)
        return {
            "status": "success",
            "message": f"Fetched {summary['total']} price records",
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prices: {str(e)}")
