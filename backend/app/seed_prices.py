
import asyncio
import random
from datetime import date
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models import Market, Commodity, Price

async def seed_prices():
    async with AsyncSessionLocal() as session:
        # Get all markets and commodities
        markets = (await session.execute(select(Market))).scalars().all()
        commodities = (await session.execute(select(Commodity))).scalars().all()
        
        print(f"Found {len(markets)} markets and {len(commodities)} commodities.")
        
        prices_added = 0
        today = date.today()
        
        for market in markets:
            # Add prices for roughly 70% of commodities per market
            for commodity in commodities:
                if random.random() > 0.3:
                    base_price = random.randint(20, 100)
                    price = Price(
                        market_id=market.id,
                        commodity_id=commodity.id,
                        price_date=today,
                        min_price=base_price - 5,
                        max_price=base_price + 5,
                        modal_price=base_price
                    )
                    session.add(price)
                    prices_added += 1
        
        await session.commit()
        print(f"Successfully added {prices_added} dummy prices for today ({today})!")

if __name__ == "__main__":
    asyncio.run(seed_prices())
