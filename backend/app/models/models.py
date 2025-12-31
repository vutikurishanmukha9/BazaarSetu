"""
BazaarSetu Backend - Database Models
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class State(Base):
    """Indian states table."""
    __tablename__ = "states"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name_telugu: Mapped[Optional[str]] = mapped_column(String(100))
    name_hindi: Mapped[Optional[str]] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    
    # Relationships
    markets: Mapped[List["Market"]] = relationship(back_populates="state")
    
    def __repr__(self) -> str:
        return f"<State(id={self.id}, name='{self.name}')>"


class Market(Base):
    """Mandi/Market locations."""
    __tablename__ = "markets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    name_telugu: Mapped[Optional[str]] = mapped_column(String(200))
    name_hindi: Mapped[Optional[str]] = mapped_column(String(200))
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    state: Mapped["State"] = relationship(back_populates="markets")
    prices: Mapped[List["Price"]] = relationship(back_populates="market")
    vendors: Mapped[List["Vendor"]] = relationship(back_populates="market")
    
    def __repr__(self) -> str:
        return f"<Market(id={self.id}, name='{self.name}', district='{self.district}')>"


class Commodity(Base):
    """Vegetables and other commodities."""
    __tablename__ = "commodities"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name_telugu: Mapped[Optional[str]] = mapped_column(String(100))
    name_hindi: Mapped[Optional[str]] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50), default="vegetable")
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    unit: Mapped[str] = mapped_column(String(20), default="kg")  # kg, dozen, piece
    
    # Relationships
    prices: Mapped[List["Price"]] = relationship(back_populates="commodity")
    alerts: Mapped[List["PriceAlert"]] = relationship(back_populates="commodity")
    
    def __repr__(self) -> str:
        return f"<Commodity(id={self.id}, name='{self.name}')>"


class Price(Base):
    """Daily price records."""
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), nullable=False)
    commodity_id: Mapped[int] = mapped_column(ForeignKey("commodities.id"), nullable=False)
    min_price: Mapped[float] = mapped_column(Float, nullable=False)
    max_price: Mapped[float] = mapped_column(Float, nullable=False)
    modal_price: Mapped[float] = mapped_column(Float, nullable=False)  # Most common price
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source: Mapped[str] = mapped_column(String(50), default="data.gov.in")
    
    # Relationships
    market: Mapped["Market"] = relationship(back_populates="prices")
    commodity: Mapped["Commodity"] = relationship(back_populates="prices")
    
    def __repr__(self) -> str:
        return f"<Price(commodity={self.commodity_id}, market={self.market_id}, modal={self.modal_price})>"


class User(Base):
    """App users for alerts and preferences."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    fcm_token: Mapped[Optional[str]] = mapped_column(String(500))  # Firebase Cloud Messaging
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")  # en, te, hi
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    alerts: Mapped[List["PriceAlert"]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, phone='{self.phone}')>"


class PriceAlert(Base):
    """User-configured price alerts."""
    __tablename__ = "price_alerts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    commodity_id: Mapped[int] = mapped_column(ForeignKey("commodities.id"), nullable=False)
    market_id: Mapped[Optional[int]] = mapped_column(ForeignKey("markets.id"))
    threshold_price: Mapped[float] = mapped_column(Float, nullable=False)
    alert_type: Mapped[str] = mapped_column(String(20), default="below")  # below, above
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_triggered: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="alerts")
    commodity: Mapped["Commodity"] = relationship(back_populates="alerts")
    
    def __repr__(self) -> str:
        return f"<PriceAlert(user={self.user_id}, commodity={self.commodity_id}, threshold={self.threshold_price})>"


class Vendor(Base):
    """Vegetable vendors/shops."""
    __tablename__ = "vendors"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    market_id: Mapped[Optional[int]] = mapped_column(ForeignKey("markets.id"))
    phone: Mapped[Optional[str]] = mapped_column(String(15))
    address: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    market: Mapped[Optional["Market"]] = relationship(back_populates="vendors")
    
    def __repr__(self) -> str:
        return f"<Vendor(id={self.id}, name='{self.name}')>"
