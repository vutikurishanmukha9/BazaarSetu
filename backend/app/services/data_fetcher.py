"""
BazaarSetu Backend - Data Fetcher Service
Fetches vegetable prices from data.gov.in and eNAM APIs
"""

import httpx
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class DataGovFetcher:
    """Fetcher for data.gov.in Agmarknet API."""
    
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    # State codes for AP and Telangana
    TARGET_STATES = ["Andhra Pradesh", "Telangana"]
    
    async def fetch_prices(
        self,
        state: Optional[str] = None,
        commodity: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Fetch current commodity prices from data.gov.in
        
        API Documentation: https://data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi
        """
        params = {
            "api-key": settings.data_gov_api_key,
            "format": "json",
            "limit": limit,
            "offset": offset
        }
        
        # Add filters if provided
        filters = []
        if state:
            filters.append(f"state={state}")
        if commodity:
            filters.append(f"commodity={commodity}")
        
        if filters:
            params["filters[0]"] = " AND ".join(filters)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                logger.info(f"Fetched {len(data.get('records', []))} records from data.gov.in")
                return data
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching from data.gov.in: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching from data.gov.in: {e}")
            raise
    
    async def fetch_ap_telangana_prices(self, commodity: Optional[str] = None) -> List[Dict]:
        """Fetch prices specifically for AP and Telangana."""
        all_records = []
        
        for state in self.TARGET_STATES:
            try:
                data = await self.fetch_prices(state=state, commodity=commodity, limit=500)
                records = data.get("records", [])
                all_records.extend(records)
            except Exception as e:
                logger.error(f"Failed to fetch prices for {state}: {e}")
                continue
        
        return all_records
    
    def parse_price_record(self, record: Dict) -> Dict:
        """Parse a raw API record into our format."""
        return {
            "state": record.get("state", ""),
            "district": record.get("district", ""),
            "market": record.get("market", ""),
            "commodity": record.get("commodity", ""),
            "variety": record.get("variety", ""),
            "min_price": float(record.get("min_price", 0)),
            "max_price": float(record.get("max_price", 0)),
            "modal_price": float(record.get("modal_price", 0)),
            "arrival_date": record.get("arrival_date", ""),
        }


class ENAMFetcher:
    """Fetcher for eNAM (Electronic National Agriculture Market) API."""
    
    BASE_URL = "https://apisetu.gov.in/enam/v1"
    
    async def fetch_commodity_prices(
        self,
        apmc_code: Optional[str] = None,
        commodity_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch prices from eNAM API."""
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if settings.enam_api_key:
            headers["X-APISETU-APIKEY"] = settings.enam_api_key
        
        params = {}
        if apmc_code:
            params["apmcCode"] = apmc_code
        if commodity_code:
            params["commodityCode"] = commodity_code
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/prices",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching from eNAM: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching from eNAM: {e}")
            raise


class PriceDataService:
    """Combined service for fetching and processing price data."""
    
    def __init__(self):
        self.data_gov_fetcher = DataGovFetcher()
        self.enam_fetcher = ENAMFetcher()
    
    async def fetch_all_prices(self) -> List[Dict]:
        """Fetch prices from all sources."""
        prices = []
        
        # Fetch from data.gov.in
        try:
            data_gov_prices = await self.data_gov_fetcher.fetch_ap_telangana_prices()
            prices.extend(data_gov_prices)
            logger.info(f"Fetched {len(data_gov_prices)} prices from data.gov.in")
        except Exception as e:
            logger.error(f"Failed to fetch from data.gov.in: {e}")
        
        # Note: eNAM API may require additional credentials
        # Add eNAM fetching here when API key is available
        
        return prices
    
    async def get_price_summary(self, records: List[Dict]) -> Dict:
        """Generate a summary of fetched prices."""
        if not records:
            return {"total": 0, "states": [], "commodities": []}
        
        states = set()
        commodities = set()
        markets = set()
        
        for record in records:
            states.add(record.get("state", ""))
            commodities.add(record.get("commodity", ""))
            markets.add(record.get("market", ""))
        
        return {
            "total": len(records),
            "states": list(states),
            "commodities": list(commodities),
            "markets_count": len(markets)
        }


# Singleton instance
price_data_service = PriceDataService()
