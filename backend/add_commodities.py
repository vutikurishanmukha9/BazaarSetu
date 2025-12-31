"""Add new commodities (chicken/eggs) to existing database"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models import Commodity

NEW_COMMODITIES = [
    {"name": "Country Chicken", "name_telugu": "నాటుకోడి", "name_hindi": "देसी मुर्गा", "category": "poultry"},
    {"name": "Broiler Chicken", "name_telugu": "బ్రాయిలర్ చికెన్", "name_hindi": "ब्रायलर मुर्गा", "category": "poultry"},
    {"name": "Chicken Boneless", "name_telugu": "బోన్‌లెస్ చికెన్", "name_hindi": "बोनलेस चिकन", "category": "poultry"},
    {"name": "Chicken Curry Cut", "name_telugu": "కర్రీ కట్ చికెన్", "name_hindi": "करी कट चिकन", "category": "poultry"},
    {"name": "Chicken Liver", "name_telugu": "చికెన్ లివర్", "name_hindi": "చికెన్ లీవర్", "category": "poultry"},
    {"name": "Eggs", "name_telugu": "గుడ్లు", "name_hindi": "अंडे", "category": "poultry"},
    {"name": "Country Eggs", "name_telugu": "నాటు గుడ్లు", "name_hindi": "देसी अंडे", "category": "poultry"},
    {"name": "Duck Eggs", "name_telugu": "బాతు గుడ్లు", "name_hindi": "बतख अंडे", "category": "poultry"},
]

async def add_commodities():
    async with AsyncSessionLocal() as session:
        # Get existing commodities
        result = await session.execute(select(Commodity))
        existing = {c.name.lower() for c in result.scalars().all()}
        
        added = 0
        for item in NEW_COMMODITIES:
            if item["name"].lower() not in existing:
                commodity = Commodity(**item)
                session.add(commodity)
                added += 1
                print(f"  + {item['name']}")
        
        await session.commit()
        print(f"\nAdded {added} new commodities")

if __name__ == "__main__":
    asyncio.run(add_commodities())
