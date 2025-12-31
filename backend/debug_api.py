"""Debug script to see what AP/Telangana data looks like"""
import asyncio
import httpx

API_KEY = "579b464db66ec23bdd0000016c8ea4c756cb4ff176ca711245797702"
URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
TARGET_STATES = ["andhra pradesh", "telangana"]

async def debug():
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
        
        print(f"Found {len(filtered)} AP/Telangana records")
        print("\n--- Commodities in API ---")
        commodities = set(r.get("commodity", "") for r in filtered)
        for c in sorted(commodities):
            print(f"  - {c}")
        
        print("\n--- Markets in API ---")
        markets = set(r.get("market", "") for r in filtered)
        for m in sorted(markets):
            print(f"  - {m}")
        
        print("\n--- Sample Records ---")
        for r in filtered[:3]:
            print(r)

asyncio.run(debug())
