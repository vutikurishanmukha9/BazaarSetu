"""
BazaarSetu Backend - Pydantic Schemas
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ==================== State Schemas ====================

class StateBase(BaseModel):
    name: str
    name_telugu: Optional[str] = None
    name_hindi: Optional[str] = None
    code: str


class StateCreate(StateBase):
    pass


class StateResponse(StateBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ==================== Market Schemas ====================

class MarketBase(BaseModel):
    name: str
    name_telugu: Optional[str] = None
    name_hindi: Optional[str] = None
    district: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class MarketCreate(MarketBase):
    state_id: int


class MarketResponse(MarketBase):
    id: int
    state_id: int
    is_active: bool
    state: Optional[StateResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ==================== Commodity Schemas ====================

class CommodityBase(BaseModel):
    name: str
    name_telugu: Optional[str] = None
    name_hindi: Optional[str] = None
    category: str = "vegetable"
    unit: str = "kg"


class CommodityCreate(CommodityBase):
    image_url: Optional[str] = None


class CommodityResponse(CommodityBase):
    id: int
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ==================== Price Schemas ====================

class PriceBase(BaseModel):
    min_price: float
    max_price: float
    modal_price: float
    price_date: date


class PriceCreate(PriceBase):
    market_id: int
    commodity_id: int
    source: str = "data.gov.in"


class PriceResponse(PriceBase):
    id: int
    market_id: int
    commodity_id: int
    fetched_at: datetime
    source: str
    commodity: Optional[CommodityResponse] = None
    market: Optional[MarketResponse] = None
    model_config = ConfigDict(from_attributes=True)


class PriceWithDetails(BaseModel):
    """Price with full commodity and market details for frontend."""
    commodity_name: str
    commodity_name_telugu: Optional[str] = None
    commodity_name_hindi: Optional[str] = None
    commodity_image: Optional[str] = None
    market_name: str
    district: str
    state_name: str
    min_price: float
    max_price: float
    modal_price: float
    price_date: date
    unit: str = "kg"
    price_change: Optional[float] = None  # % change from yesterday


# ==================== Price Trend Schemas ====================

class PriceTrendPoint(BaseModel):
    date: date
    modal_price: float


class PriceTrend(BaseModel):
    commodity_id: int
    commodity_name: str
    market_id: Optional[int] = None
    market_name: Optional[str] = None
    trend_data: List[PriceTrendPoint]
    avg_price: float
    min_price: float
    max_price: float
    price_change_7d: Optional[float] = None  # % change over 7 days
    price_change_30d: Optional[float] = None  # % change over 30 days


# ==================== User Schemas ====================

class UserBase(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_language: str = "en"


class UserCreate(UserBase):
    fcm_token: Optional[str] = None


class UserResponse(UserBase):
    id: int
    push_enabled: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==================== Price Alert Schemas ====================

class PriceAlertBase(BaseModel):
    commodity_id: int
    market_id: Optional[int] = None
    threshold_price: float
    alert_type: str = "below"  # below, above


class PriceAlertCreate(PriceAlertBase):
    user_id: int


class PriceAlertResponse(PriceAlertBase):
    id: int
    user_id: int
    is_active: bool
    last_triggered: Optional[datetime] = None
    created_at: datetime
    commodity: Optional[CommodityResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ==================== Vendor Schemas ====================

class VendorBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float


class VendorCreate(VendorBase):
    market_id: Optional[int] = None


class VendorResponse(VendorBase):
    id: int
    market_id: Optional[int] = None
    is_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==================== API Response Wrappers ====================

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


class MarketComparison(BaseModel):
    """Compare prices across markets for a commodity."""
    commodity_id: int
    commodity_name: str
    price_date: date
    markets: List[dict]  # [{market_name, district, modal_price, min_price, max_price}]
