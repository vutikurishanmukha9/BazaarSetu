"""
BazaarSetu Backend - Price Service
Business logic for price queries, trends, and comparisons
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Dict
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging

from app.models import Price, Commodity, Market, State
from app.schemas import PriceWithDetails, PriceTrend, PriceTrendPoint, MarketComparison

logger = logging.getLogger(__name__)


class PriceService:
    """Service for price-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_today_prices(
        self,
        state_id: Optional[int] = None,
        commodity_id: Optional[int] = None,
        market_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 50
    ) -> List[PriceWithDetails]:
        """Get today's prices with optional filters."""
        
        today = date.today()
        
        query = (
            select(Price)
            .options(
                selectinload(Price.commodity),
                selectinload(Price.market).selectinload(Market.state)
            )
            .where(Price.price_date == today)
            .order_by(desc(Price.modal_price))
        )
        
        # Apply filters
        if commodity_id:
            query = query.where(Price.commodity_id == commodity_id)
        if market_id:
            query = query.where(Price.market_id == market_id)
        if state_id:
            query = query.join(Market).where(Market.state_id == state_id)
        
        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        # Get yesterday's prices for price change calculation
        yesterday = today - timedelta(days=1)
        yesterday_prices = await self._get_prices_by_date(yesterday)
        yesterday_map = {
            (p.commodity_id, p.market_id): p.modal_price 
            for p in yesterday_prices
        }
        
        # Convert to response schema
        response = []
        for price in prices:
            yesterday_price = yesterday_map.get((price.commodity_id, price.market_id))
            price_change = None
            if yesterday_price and yesterday_price > 0:
                price_change = ((price.modal_price - yesterday_price) / yesterday_price) * 100
            
            response.append(PriceWithDetails(
                commodity_name=price.commodity.name,
                commodity_name_telugu=price.commodity.name_telugu,
                commodity_name_hindi=price.commodity.name_hindi,
                commodity_image=price.commodity.image_url,
                market_name=price.market.name,
                district=price.market.district,
                state_name=price.market.state.name,
                min_price=price.min_price,
                max_price=price.max_price,
                modal_price=price.modal_price,
                price_date=price.price_date,
                unit=price.commodity.unit,
                price_change=round(price_change, 2) if price_change else None
            ))
        
        return response
    
    async def _get_prices_by_date(self, target_date: date) -> List[Price]:
        """Get all prices for a specific date."""
        query = select(Price).where(Price.price_date == target_date)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_price_trend(
        self,
        commodity_id: int,
        market_id: Optional[int] = None,
        days: int = 30
    ) -> PriceTrend:
        """Get price trend for a commodity over specified days."""
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        query = (
            select(Price)
            .options(selectinload(Price.commodity), selectinload(Price.market))
            .where(
                and_(
                    Price.commodity_id == commodity_id,
                    Price.price_date >= start_date,
                    Price.price_date <= end_date
                )
            )
            .order_by(Price.price_date)
        )
        
        if market_id:
            query = query.where(Price.market_id == market_id)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            raise ValueError(f"No prices found for commodity {commodity_id}")
        
        # Aggregate by date (average across markets if no market specified)
        date_prices: Dict[date, List[float]] = {}
        for price in prices:
            if price.price_date not in date_prices:
                date_prices[price.price_date] = []
            date_prices[price.price_date].append(price.modal_price)
        
        trend_data = [
            PriceTrendPoint(date=d, modal_price=sum(p)/len(p))
            for d, p in sorted(date_prices.items())
        ]
        
        all_prices = [p.modal_price for p in prices]
        avg_price = sum(all_prices) / len(all_prices)
        
        # Calculate price changes
        price_7d = None
        price_30d = None
        
        if len(trend_data) >= 2:
            latest = trend_data[-1].modal_price
            
            # 7 day change
            if len(trend_data) >= 7:
                price_7_ago = trend_data[-7].modal_price
                if price_7_ago > 0:
                    price_7d = ((latest - price_7_ago) / price_7_ago) * 100
            
            # 30 day change
            if len(trend_data) >= 30:
                price_30_ago = trend_data[0].modal_price
                if price_30_ago > 0:
                    price_30d = ((latest - price_30_ago) / price_30_ago) * 100
        
        commodity = prices[0].commodity
        market = prices[0].market if market_id else None
        
        return PriceTrend(
            commodity_id=commodity_id,
            commodity_name=commodity.name,
            market_id=market_id,
            market_name=market.name if market else None,
            trend_data=trend_data,
            avg_price=round(avg_price, 2),
            min_price=min(all_prices),
            max_price=max(all_prices),
            price_change_7d=round(price_7d, 2) if price_7d else None,
            price_change_30d=round(price_30d, 2) if price_30d else None
        )
    
    async def compare_markets(
        self,
        commodity_id: int,
        target_date: Optional[date] = None
    ) -> MarketComparison:
        """Compare prices across different markets for a commodity."""
        
        if not target_date:
            target_date = date.today()
        
        query = (
            select(Price)
            .options(
                selectinload(Price.commodity),
                selectinload(Price.market).selectinload(Market.state)
            )
            .where(
                and_(
                    Price.commodity_id == commodity_id,
                    Price.price_date == target_date
                )
            )
            .order_by(Price.modal_price)
        )
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            raise ValueError(f"No prices found for commodity {commodity_id} on {target_date}")
        
        markets = [
            {
                "market_id": p.market_id,
                "market_name": p.market.name,
                "district": p.market.district,
                "state": p.market.state.name,
                "min_price": p.min_price,
                "max_price": p.max_price,
                "modal_price": p.modal_price
            }
            for p in prices
        ]
        
        return MarketComparison(
            commodity_id=commodity_id,
            commodity_name=prices[0].commodity.name,
            price_date=target_date,
            markets=markets
        )
    
    async def search_commodities(
        self,
        query: str,
        limit: int = 20
    ) -> List[Commodity]:
        """Search commodities by name."""
        
        search_query = (
            select(Commodity)
            .where(
                Commodity.name.ilike(f"%{query}%") |
                Commodity.name_telugu.ilike(f"%{query}%") |
                Commodity.name_hindi.ilike(f"%{query}%")
            )
            .limit(limit)
        )
        
        result = await self.db.execute(search_query)
        return result.scalars().all()
