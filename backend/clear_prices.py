"""Clear all prices and refetch real ones"""
import asyncio
from sqlalchemy import delete
from app.core.database import AsyncSessionLocal
from app.models import Price

async def clear_prices():
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Price))
        await session.commit()
        print(f"🗑️ Cleared all price records from database!")

if __name__ == "__main__":
    asyncio.run(clear_prices())
