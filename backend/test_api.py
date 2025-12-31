"""Test data.gov.in API"""
import httpx
import asyncio

API_KEY = "579b464db66ec23bdd0000016c8ea4c756cb4ff176ca711245797702"
URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

async def test_api():
    async with httpx.AsyncClient(timeout=30) as client:
        # Test without filters
        response = await client.get(URL, params={
            "api-key": API_KEY,
            "format": "json",
            "limit": 10
        })
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Total records available: {data.get('total', 'N/A')}")
        print(f"Records returned: {len(data.get('records', []))}")
        
        if data.get('records'):
            print("\nSample record:")
            print(data['records'][0])
        else:
            print("\nNo records found. Response:")
            print(data)

if __name__ == "__main__":
    asyncio.run(test_api())
