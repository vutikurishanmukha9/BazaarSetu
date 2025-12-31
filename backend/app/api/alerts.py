"""
BazaarSetu Backend - Alerts API Routes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import AlertService
from app.schemas import PriceAlertCreate, PriceAlertResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/", response_model=PriceAlertResponse)
async def create_alert(
    alert_data: PriceAlertCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new price alert.
    
    Alert types:
    - `below`: Notify when price drops below threshold
    - `above`: Notify when price rises above threshold
    """
    service = AlertService(db)
    alert = await service.create_alert(alert_data)
    return PriceAlertResponse.model_validate(alert)


@router.get("/user/{user_id}", response_model=List[PriceAlertResponse])
async def get_user_alerts(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all alerts for a user."""
    service = AlertService(db)
    alerts = await service.get_user_alerts(user_id)
    return [PriceAlertResponse.model_validate(a) for a in alerts]


@router.patch("/{alert_id}/toggle")
async def toggle_alert(
    alert_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Toggle an alert's active status."""
    service = AlertService(db)
    alert = await service.toggle_alert(alert_id, user_id)
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "id": alert.id,
        "is_active": alert.is_active,
        "message": f"Alert {'activated' if alert.is_active else 'deactivated'}"
    }


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an alert."""
    service = AlertService(db)
    deleted = await service.delete_alert(alert_id, user_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert deleted successfully"}
