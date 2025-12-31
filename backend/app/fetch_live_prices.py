"""
BazaarSetu Backend - Fetch and Store Live Prices
Fetches real prices from data.gov.in and stores them in the database.
"""

import asyncio
import httpx
from datetime import date, datetime
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import Market, Commodity, Price
from app.core.config import get_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()

TARGET_STATES = ["andhra pradesh", "telangana"]
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


async def fetch_from_api(limit=2000):
    """Fetch prices directly from data.gov.in API."""
    print(f"📡 Fetching up to {limit} records from data.gov.in...")
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(API_URL, params={
            "api-key": settings.data_gov_api_key,
            "format": "json",
            "limit": limit
        })
        response.raise_for_status()
        data = response.json()
        
        total = data.get("total", 0)
        records = data.get("records", [])
        print(f"📊 Total available: {total}, Fetched: {len(records)}")
        return records


async def fetch_and_store_prices():
    """Fetch live prices from API and store in database."""
    
    print("🚀 Starting live price fetch...")
    
    # Step 1: Fetch from API
    try:
        all_records = await fetch_from_api(limit=2000)
    except Exception as e:
        print(f"❌ Failed to fetch from API: {e}")
        return
    
    if not all_records:
        print("⚠️ No records returned from API.")
        return
    
    # Filter for AP and Telangana only
    records = [
        r for r in all_records 
        if r.get("state", "").lower() in TARGET_STATES
    ]
    print(f"🎯 Filtered to {len(records)} records for AP & Telangana")
    
    if not records:
        print("⚠️ No records found for AP/Telangana in API data.")
        return
    
    # Step 2: Store in database
    async with AsyncSessionLocal() as session:
        # Get existing markets and commodities for mapping
        markets_result = await session.execute(select(Market))
        markets = {m.name.lower(): m for m in markets_result.scalars().all()}
        
        commodities_result = await session.execute(select(Commodity))
        commodities = {c.name.lower(): c for c in commodities_result.scalars().all()}
        
        print(f"📋 DB has {len(markets)} markets, {len(commodities)} commodities")
        
        prices_added = 0
        prices_skipped = 0
        today = date.today()
        
        for record in records:
            try:
                # Match commodity with fuzzy matching
                api_commodity = record.get("commodity", "").lower().strip()
                commodity = None
                
                # Try exact match first
                for cname, c in commodities.items():
                    if cname == api_commodity:
                        commodity = c
                        break
                
                # Try word matching (e.g., "Ridgeguard(Torai)" matches "Ridge Gourd")
                if not commodity:
                    api_words = set(api_commodity.replace("(", " ").replace(")", " ").split())
                    for cname, c in commodities.items():
                        db_words = set(cname.split())
                        # Check if any significant word matches
                        common = api_words & db_words
                        if common and len(common) >= 1:
                            commodity = c
                            break
                        # Check substring
                        for word in db_words:
                            if len(word) > 3 and word in api_commodity:
                                commodity = c
                                break
                        if commodity:
                            break
                
                if not commodity:
                    prices_skipped += 1
                    continue
                
                # Match market with fuzzy matching
                api_market = record.get("market", "").lower().strip()
                market = None
                
                # Remove common suffixes
                api_market_clean = api_market.replace(" apmc", "").replace(" market", "").strip()
                
                for mname, m in markets.items():
                    mname_clean = mname.replace(" apmc", "").replace(" market", "").strip()
                    if mname_clean == api_market_clean:
                        market = m
                        break
                    if mname_clean in api_market_clean or api_market_clean in mname_clean:
                        market = m
                        break
                
                if not market:
                    prices_skipped += 1
                    continue
                
                # Parse date
                arrival_date_str = record.get("arrival_date", "")
                try:
                    price_date = datetime.strptime(arrival_date_str, "%d/%m/%Y").date() if arrival_date_str else today
                except:
                    price_date = today
                
                # Parse prices
                min_price = float(record.get("min_price", 0) or 0)
                max_price = float(record.get("max_price", 0) or 0)
                modal_price = float(record.get("modal_price", 0) or 0)
                
                if modal_price <= 0:
                    prices_skipped += 1
                    continue
                
                # Create and add price record
                price = Price(
                    market_id=market.id,
                    commodity_id=commodity.id,
                    price_date=price_date,
                    min_price=min_price,
                    max_price=max_price,
                    modal_price=modal_price,
                    source="data.gov.in"
                )
                session.add(price)
                prices_added += 1
                
            except Exception as e:
                logger.error(f"Error processing record: {e}")
                prices_skipped += 1
                continue
        
        await session.commit()
        print(f"✅ Added {prices_added} real price records!")
        print(f"⏭️ Skipped {prices_skipped} (no matching commodity/market in DB)")


if __name__ == "__main__":
    asyncio.run(fetch_and_store_prices())
