"""
BazaarSetu - Comprehensive Dummy Data Generator
Creates 30 days of historical price data for testing trends and charts.
"""

import asyncio
import random
from datetime import date, timedelta
from sqlalchemy import select, delete
from app.core.database import AsyncSessionLocal
from app.models import Market, Commodity, Price

# Base prices for each commodity (realistic values)
BASE_PRICES = {
    "tomato": 40,
    "onion": 35,
    "potato": 30,
    "green chilli": 80,
    "brinjal": 45,
    "cabbage": 25,
    "cauliflower": 50,
    "carrot": 55,
    "beans": 70,
    "lady finger": 60,
    "bottle gourd": 35,
    "ridge gourd": 40,
    "bitter gourd": 65,
    "drumstick": 90,
    "cucumber": 30,
    "spinach": 40,
    "coriander": 100,
    "mint": 80,
    "garlic": 200,
    "ginger": 180,
    "methi": 60,
    "capsicum": 80,
    "coconut": 25,
    "banana": 50,
    "lemon": 120,
    "pumpkin": 30,
    "curry leaves": 150,
    # Poultry
    "country chicken": 450,
    "broiler chicken": 180,
    "chicken boneless": 350,
    "chicken curry cut": 220,
    "chicken liver": 180,
    "eggs": 6,  # per piece
    "country eggs": 12,
    "duck eggs": 15,
}


async def seed_historical_data():
    """Generate 30 days of price history for all markets and commodities."""
    
    print("🌱 Seeding comprehensive historical price data...")
    
    async with AsyncSessionLocal() as session:
        # Clear existing prices
        await session.execute(delete(Price))
        print("🗑️ Cleared existing prices")
        
        # Get all markets and commodities
        markets = (await session.execute(select(Market))).scalars().all()
        commodities = (await session.execute(select(Commodity))).scalars().all()
        
        print(f"📊 Found {len(markets)} markets, {len(commodities)} commodities")
        
        today = date.today()
        prices_added = 0
        
        # Generate prices for the past 30 days
        for day_offset in range(30, -1, -1):  # 30 days ago to today
            price_date = today - timedelta(days=day_offset)
            
            for market in markets:
                # Each market reports ~80% of commodities on any given day
                for commodity in commodities:
                    if random.random() > 0.2:  # 80% chance to have data
                        # Get base price or use default
                        base = BASE_PRICES.get(commodity.name.lower(), 50)
                        
                        # Add daily variation (-15% to +15%)
                        daily_factor = 1 + random.uniform(-0.15, 0.15)
                        
                        # Add trend over time (slight increase or decrease)
                        trend_factor = 1 + (random.uniform(-0.005, 0.01) * (30 - day_offset))
                        
                        # Add market-specific variation
                        market_factor = 1 + random.uniform(-0.1, 0.1)
                        
                        modal_price = base * daily_factor * trend_factor * market_factor
                        modal_price = round(modal_price, 0)
                        
                        min_price = modal_price - random.randint(3, 10)
                        max_price = modal_price + random.randint(3, 10)
                        
                        price = Price(
                            market_id=market.id,
                            commodity_id=commodity.id,
                            price_date=price_date,
                            min_price=max(5, min_price),
                            max_price=max_price,
                            modal_price=modal_price,
                            source="seed_data"
                        )
                        session.add(price)
                        prices_added += 1
        
        await session.commit()
        print(f"✅ Added {prices_added} price records for 30 days!")
        print(f"📅 Date range: {today - timedelta(days=30)} to {today}")


if __name__ == "__main__":
    asyncio.run(seed_historical_data())
