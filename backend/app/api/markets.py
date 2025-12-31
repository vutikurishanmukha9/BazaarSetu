"""
BazaarSetu Backend - Markets & Commodities API Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import State, Market, Commodity
from app.schemas import StateResponse, MarketResponse, CommodityResponse

router = APIRouter(tags=["Markets & Commodities"])


# ==================== States ====================

@router.get("/states", response_model=List[StateResponse])
async def get_states(db: AsyncSession = Depends(get_db)):
    """Get all available states."""
    result = await db.execute(select(State).order_by(State.name))
    states = result.scalars().all()
    return [StateResponse.model_validate(s) for s in states]


@router.get("/states/{state_id}", response_model=StateResponse)
async def get_state(state_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific state by ID."""
    result = await db.execute(select(State).where(State.id == state_id))
    state = result.scalar_one_or_none()
    
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    
    return StateResponse.model_validate(state)


# ==================== Markets ====================

@router.get("/markets", response_model=List[MarketResponse])
async def get_markets(
    state_id: Optional[int] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    db: AsyncSession = Depends(get_db)
):
    """Get all markets with optional filters."""
    query = select(Market).options(selectinload(Market.state)).where(Market.is_active == True)
    
    if state_id:
        query = query.where(Market.state_id == state_id)
    if district:
        query = query.where(Market.district.ilike(f"%{district}%"))
    
    query = query.order_by(Market.name)
    
    result = await db.execute(query)
    markets = result.scalars().all()
    return [MarketResponse.model_validate(m) for m in markets]


@router.get("/markets/{market_id}", response_model=MarketResponse)
async def get_market(market_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific market by ID."""
    result = await db.execute(
        select(Market)
        .options(selectinload(Market.state))
        .where(Market.id == market_id)
    )
    market = result.scalar_one_or_none()
    
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    
    return MarketResponse.model_validate(market)


# ==================== Commodities ====================

@router.get("/commodities", response_model=List[CommodityResponse])
async def get_commodities(
    category: Optional[str] = Query(None, description="Filter by category (vegetable, fruit, etc.)"),
    db: AsyncSession = Depends(get_db)
):
    """Get all commodities with optional category filter."""
    query = select(Commodity)
    
    if category:
        query = query.where(Commodity.category == category)
    
    query = query.order_by(Commodity.name)
    
    result = await db.execute(query)
    commodities = result.scalars().all()
    return [CommodityResponse.model_validate(c) for c in commodities]


@router.get("/commodities/{commodity_id}", response_model=CommodityResponse)
async def get_commodity(commodity_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific commodity by ID."""
    result = await db.execute(select(Commodity).where(Commodity.id == commodity_id))
    commodity = result.scalar_one_or_none()
    
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    
    return CommodityResponse.model_validate(commodity)
