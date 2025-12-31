"""
BazaarSetu Backend - Seed Data for AP & Telangana
Run this script to populate initial data
"""

import asyncio
from app.core.database import AsyncSessionLocal, init_db
from app.models import State, Market, Commodity


# AP & Telangana States
STATES = [
    {"name": "Andhra Pradesh", "name_telugu": "ఆంధ్ర ప్రదేశ్", "name_hindi": "आंध्र प्रदेश", "code": "AP"},
    {"name": "Telangana", "name_telugu": "తెలంగాణ", "name_hindi": "तेलंगाना", "code": "TS"},
]

# Major Markets in AP & Telangana
MARKETS = [
    # Andhra Pradesh Markets
    {"name": "Vijayawada", "name_telugu": "విజయవాడ", "district": "Krishna", "state_code": "AP", "lat": 16.5062, "lon": 80.6480},
    {"name": "Visakhapatnam", "name_telugu": "విశాఖపట్నం", "district": "Visakhapatnam", "state_code": "AP", "lat": 17.6868, "lon": 83.2185},
    {"name": "Guntur", "name_telugu": "గుంటూరు", "district": "Guntur", "state_code": "AP", "lat": 16.3067, "lon": 80.4365},
    {"name": "Tirupati", "name_telugu": "తిరుపతి", "district": "Chittoor", "state_code": "AP", "lat": 13.6288, "lon": 79.4192},
    {"name": "Nellore", "name_telugu": "నెల్లూరు", "district": "Nellore", "state_code": "AP", "lat": 14.4426, "lon": 79.9865},
    {"name": "Kurnool", "name_telugu": "కర్నూలు", "district": "Kurnool", "state_code": "AP", "lat": 15.8281, "lon": 78.0373},
    {"name": "Rajahmundry", "name_telugu": "రాజమండ్రి", "district": "East Godavari", "state_code": "AP", "lat": 16.9891, "lon": 81.7801},
    {"name": "Kadapa", "name_telugu": "కడప", "district": "Kadapa", "state_code": "AP", "lat": 14.4673, "lon": 78.8242},
    {"name": "Anantapur", "name_telugu": "అనంతపురం", "district": "Anantapur", "state_code": "AP", "lat": 14.6819, "lon": 77.6006},
    {"name": "Eluru", "name_telugu": "ఏలూరు", "district": "West Godavari", "state_code": "AP", "lat": 16.7107, "lon": 81.0952},
    
    # Telangana Markets
    {"name": "Hyderabad", "name_telugu": "హైదరాబాద్", "district": "Hyderabad", "state_code": "TS", "lat": 17.3850, "lon": 78.4867},
    {"name": "Secunderabad", "name_telugu": "సికిందరాబాద్", "district": "Hyderabad", "state_code": "TS", "lat": 17.4399, "lon": 78.4983},
    {"name": "Warangal", "name_telugu": "వరంగల్", "district": "Warangal", "state_code": "TS", "lat": 17.9689, "lon": 79.5941},
    {"name": "Karimnagar", "name_telugu": "కరీంనగర్", "district": "Karimnagar", "state_code": "TS", "lat": 18.4386, "lon": 79.1288},
    {"name": "Nizamabad", "name_telugu": "నిజామాబాద్", "district": "Nizamabad", "state_code": "TS", "lat": 18.6725, "lon": 78.0941},
    {"name": "Khammam", "name_telugu": "ఖమ్మం", "district": "Khammam", "state_code": "TS", "lat": 17.2473, "lon": 80.1514},
    {"name": "Mahabubnagar", "name_telugu": "మహబూబ్‌నగర్", "district": "Mahabubnagar", "state_code": "TS", "lat": 16.7488, "lon": 77.9853},
    {"name": "Nalgonda", "name_telugu": "నల్గొండ", "district": "Nalgonda", "state_code": "TS", "lat": 17.0575, "lon": 79.2690},
    {"name": "Adilabad", "name_telugu": "ఆదిలాబాద్", "district": "Adilabad", "state_code": "TS", "lat": 19.6640, "lon": 78.5320},
    {"name": "Medak", "name_telugu": "మెదక్", "district": "Medak", "state_code": "TS", "lat": 18.0469, "lon": 78.2600},
]

# Common Vegetables
COMMODITIES = [
    {"name": "Tomato", "name_telugu": "టమాటా", "name_hindi": "टमाटर", "category": "vegetable"},
    {"name": "Onion", "name_telugu": "ఉల్లిపాయ", "name_hindi": "प्याज", "category": "vegetable"},
    {"name": "Potato", "name_telugu": "బంగాళాదుంప", "name_hindi": "आलू", "category": "vegetable"},
    {"name": "Green Chilli", "name_telugu": "పచ్చిమిర్చి", "name_hindi": "हरी मिर्च", "category": "vegetable"},
    {"name": "Brinjal", "name_telugu": "వంకాయ", "name_hindi": "बैंगन", "category": "vegetable"},
    {"name": "Cabbage", "name_telugu": "క్యాబేజ్", "name_hindi": "पत्ता गोभी", "category": "vegetable"},
    {"name": "Cauliflower", "name_telugu": "కాలీఫ్లవర్", "name_hindi": "फूलगोभी", "category": "vegetable"},
    {"name": "Carrot", "name_telugu": "క్యారెట్", "name_hindi": "गाजर", "category": "vegetable"},
    {"name": "Beans", "name_telugu": "చిక్కుడు", "name_hindi": "फलियां", "category": "vegetable"},
    {"name": "Lady Finger", "name_telugu": "బెండకాయ", "name_hindi": "भिंडी", "category": "vegetable"},
    {"name": "Bottle Gourd", "name_telugu": "సొరకాయ", "name_hindi": "लौकी", "category": "vegetable"},
    {"name": "Ridge Gourd", "name_telugu": "బీరకాయ", "name_hindi": "तोरई", "category": "vegetable"},
    {"name": "Bitter Gourd", "name_telugu": "కాకరకాయ", "name_hindi": "करेला", "category": "vegetable"},
    {"name": "Drumstick", "name_telugu": "మునగకాయ", "name_hindi": "सहजन", "category": "vegetable"},
    {"name": "Cucumber", "name_telugu": "దోసకాయ", "name_hindi": "खीरा", "category": "vegetable"},
    {"name": "Pumpkin", "name_telugu": "గుమ్మడికాయ", "name_hindi": "कद्दू", "category": "vegetable"},
    {"name": "Spinach", "name_telugu": "పాలకూర", "name_hindi": "पालक", "category": "leafy"},
    {"name": "Methi", "name_telugu": "మెంతికూర", "name_hindi": "मेथी", "category": "leafy"},
    {"name": "Coriander", "name_telugu": "కొత్తిమీర", "name_hindi": "धनिया", "category": "leafy"},
    {"name": "Curry Leaves", "name_telugu": "కరివేపాకు", "name_hindi": "करी पत्ता", "category": "leafy"},
    {"name": "Ginger", "name_telugu": "అల్లం", "name_hindi": "अदरक", "category": "spice"},
    {"name": "Garlic", "name_telugu": "వెల్లుల్లి", "name_hindi": "लहसुन", "category": "spice"},
    {"name": "Lemon", "name_telugu": "నిమ్మకాయ", "name_hindi": "नींबू", "category": "fruit"},
    {"name": "Coconut", "name_telugu": "కొబ్బరి", "name_hindi": "नारियल", "category": "fruit"},
    {"name": "Banana", "name_telugu": "అరటిపళ్ళు", "name_hindi": "केला", "category": "fruit"},
]


async def seed_database():
    """Seed the database with initial data."""
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Add States
        state_map = {}
        for state_data in STATES:
            state = State(**state_data)
            session.add(state)
            await session.flush()
            state_map[state_data["code"]] = state.id
        
        # Add Markets
        for market_data in MARKETS:
            state_code = market_data.pop("state_code")
            lat = market_data.pop("lat")
            lon = market_data.pop("lon")
            
            market = Market(
                **market_data,
                state_id=state_map[state_code],
                latitude=lat,
                longitude=lon
            )
            session.add(market)
        
        # Add Commodities
        for commodity_data in COMMODITIES:
            commodity = Commodity(**commodity_data)
            session.add(commodity)
        
        await session.commit()
        print("Database seeded successfully!")
        print(f"   - {len(STATES)} states")
        print(f"   - {len(MARKETS)} markets")
        print(f"   - {len(COMMODITIES)} commodities")


if __name__ == "__main__":
    asyncio.run(seed_database())
