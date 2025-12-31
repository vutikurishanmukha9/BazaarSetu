"""Add markets from API to database"""
import asyncio
import httpx
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import Market, State

API_KEY = "579b464db66ec23bdd0000016c8ea4c756cb4ff176ca711245797702"
URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
TARGET_STATES = ["andhra pradesh", "telangana"]

async def add_markets():
    # Fetch from API
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(URL, params={
            "api-key": API_KEY,
            "format": "json",
            "limit": 2000
        })
        data = response.json()
        records = data.get("records", [])
    
    # Filter for AP/Telangana
    filtered = [r for r in records if r.get("state", "").lower() in TARGET_STATES]
    
    # Get unique markets from API
    api_markets = {}
    for r in filtered:
        market_name = r.get("market", "").strip()
        state_name = r.get("state", "").strip()
        district = r.get("district", "").strip()
        if market_name and market_name not in api_markets:
            api_markets[market_name] = {"state": state_name, "district": district}
    
    print(f"Found {len(api_markets)} unique markets in API for AP/Telangana")
    
    async with AsyncSessionLocal() as session:
        # Get state IDs
        states_result = await session.execute(select(State))
        states = {s.name.lower(): s.id for s in states_result.scalars().all()}
        
        # Get existing markets
        markets_result = await session.execute(select(Market))
        existing = {m.name.lower() for m in markets_result.scalars().all()}
        
        added = 0
        for market_name, info in api_markets.items():
            clean_name = market_name.replace(" APMC", "").strip()
            if clean_name.lower() not in existing and market_name.lower() not in existing:
                state_id = states.get(info["state"].lower(), 1)
                market = Market(
                    name=clean_name,
                    district=info["district"],
                    state_id=state_id,
                    is_active=True
                )
                session.add(market)
                added += 1
                print(f"  + {clean_name} ({info['district']})")
        
        await session.commit()
        print(f"\n✅ Added {added} new markets to database")

if __name__ == "__main__":
    asyncio.run(add_markets())
