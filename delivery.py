from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Order, Delivery
from schemas import DeliveryStatusUpdate
from auth import get_current_delivery_partner
from fastapi import Depends

router = APIRouter()

@router.put("/deliveries/{delivery_id}/status", dependencies=[Depends(get_current_delivery_partner)])
async def update_delivery_status(delivery_id: int, status: str):
    # Placeholder code to update the delivery status
    return {"msg": f"Delivery with ID {delivery_id} status updated to {status}."}

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Update Delivery Status
@router.put("/deliveries/{order_id}/status", dependencies=[Depends(get_current_delivery_partner)])
async def update_delivery_status(order_id: int, status_update: DeliveryStatusUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_delivery_partner)):
    # Retrieve the order and ensure it exists
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update or create delivery entry with status and comment
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if not delivery:
        delivery = Delivery(order_id=order_id, user_id=current_user.id, status=status_update.status, comment=status_update.comment)
        db.add(delivery)
    else:
        delivery.status = status_update.status
        if status_update.comment:
            delivery.comment = status_update.comment
    db.commit()
    db.refresh(delivery)
    return {"msg": "Delivery status updated", "order_id": order_id, "status": delivery.status, "comment": delivery.comment}

@router.put("/deliveries/{delivery_id}/comment", dependencies=[Depends(get_current_delivery_partner)])
async def add_delivery_comment(delivery_id: int, comment: str):
    # Placeholder code to add a comment to the delivery
    return {"msg": f"Comment added to delivery ID {delivery_id}."}