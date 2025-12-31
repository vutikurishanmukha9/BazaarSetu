"""
BazaarSetu Backend - Alert Service
Manages price alerts and push notifications
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging

from app.models import PriceAlert, Price, User, Commodity
from app.schemas import PriceAlertCreate, PriceAlertResponse

logger = logging.getLogger(__name__)


class AlertService:
    """Service for managing price alerts."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_alert(self, alert_data: PriceAlertCreate) -> PriceAlert:
        """Create a new price alert."""
        
        alert = PriceAlert(
            user_id=alert_data.user_id,
            commodity_id=alert_data.commodity_id,
            market_id=alert_data.market_id,
            threshold_price=alert_data.threshold_price,
            alert_type=alert_data.alert_type,
            is_active=True
        )
        
        self.db.add(alert)
        await self.db.commit()
        await self.db.refresh(alert)
        
        logger.info(f"Created alert {alert.id} for user {alert.user_id}")
        return alert
    
    async def get_user_alerts(self, user_id: int) -> List[PriceAlert]:
        """Get all alerts for a user."""
        
        query = (
            select(PriceAlert)
            .options(selectinload(PriceAlert.commodity))
            .where(PriceAlert.user_id == user_id)
            .order_by(PriceAlert.created_at.desc())
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def toggle_alert(self, alert_id: int, user_id: int) -> Optional[PriceAlert]:
        """Toggle an alert's active status."""
        
        query = select(PriceAlert).where(
            and_(
                PriceAlert.id == alert_id,
                PriceAlert.user_id == user_id
            )
        )
        
        result = await self.db.execute(query)
        alert = result.scalar_one_or_none()
        
        if alert:
            alert.is_active = not alert.is_active
            await self.db.commit()
            await self.db.refresh(alert)
        
        return alert
    
    async def delete_alert(self, alert_id: int, user_id: int) -> bool:
        """Delete an alert."""
        
        query = select(PriceAlert).where(
            and_(
                PriceAlert.id == alert_id,
                PriceAlert.user_id == user_id
            )
        )
        
        result = await self.db.execute(query)
        alert = result.scalar_one_or_none()
        
        if alert:
            await self.db.delete(alert)
            await self.db.commit()
            return True
        
        return False
    
    async def check_and_trigger_alerts(self, prices: List[Price]) -> List[dict]:
        """
        Check if any alerts should be triggered based on new prices.
        Returns list of triggered alerts with user info for notification.
        """
        
        triggered = []
        
        for price in prices:
            # Find matching alerts
            query = (
                select(PriceAlert)
                .options(selectinload(PriceAlert.user))
                .where(
                    and_(
                        PriceAlert.commodity_id == price.commodity_id,
                        PriceAlert.is_active == True,
                        # Either no specific market or matching market
                        (PriceAlert.market_id == None) | 
                        (PriceAlert.market_id == price.market_id)
                    )
                )
            )
            
            result = await self.db.execute(query)
            alerts = result.scalars().all()
            
            for alert in alerts:
                should_trigger = False
                
                if alert.alert_type == "below":
                    should_trigger = price.modal_price <= alert.threshold_price
                elif alert.alert_type == "above":
                    should_trigger = price.modal_price >= alert.threshold_price
                
                if should_trigger:
                    # Update last triggered
                    alert.last_triggered = datetime.utcnow()
                    
                    triggered.append({
                        "alert_id": alert.id,
                        "user_id": alert.user_id,
                        "fcm_token": alert.user.fcm_token if alert.user else None,
                        "commodity_id": price.commodity_id,
                        "market_id": price.market_id,
                        "current_price": price.modal_price,
                        "threshold_price": alert.threshold_price,
                        "alert_type": alert.alert_type
                    })
        
        if triggered:
            await self.db.commit()
            logger.info(f"Triggered {len(triggered)} price alerts")
        
        return triggered


async def send_push_notification(fcm_token: str, title: str, body: str) -> bool:
    """
    Send push notification via Firebase Cloud Messaging.
    
    Note: Requires firebase-admin to be configured with credentials.
    """
    try:
        # TODO: Implement when Firebase is configured
        # from firebase_admin import messaging
        # message = messaging.Message(
        #     notification=messaging.Notification(title=title, body=body),
        #     token=fcm_token
        # )
        # response = messaging.send(message)
        logger.info(f"Would send notification to {fcm_token[:20]}...")
        return True
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")
        return False
