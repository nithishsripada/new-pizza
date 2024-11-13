from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from auth import get_current_admin
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Pizza, Order
from schemas import PizzaCreate, PizzaUpdate, OrderStatusUpdate


router = APIRouter()

@router.post("/pizzas/", response_model=PizzaCreate, dependencies=[Depends(get_current_admin)])
async def create_pizza(pizza: PizzaCreate):
    # Placeholder code to add pizza
    return pizza

@router.put("/pizzas/{pizza_id}", response_model=PizzaCreate, dependencies=[Depends(get_current_admin)])
async def update_pizza(pizza_id: int, pizza: PizzaCreate):
    # Placeholder code to update pizza details
    return pizza

@router.delete("/pizzas/{pizza_id}", dependencies=[Depends(get_current_admin)])
async def delete_pizza(pizza_id: int):
    # Placeholder code to delete a pizza
    return {"msg": f"Pizza with ID {pizza_id} deleted."}

@router.put("/orders/{order_id}/status", dependencies=[Depends(get_current_admin)])
async def update_order_status(order_id: int, status: str):
    # Placeholder code to update order status
    return {"msg": f"Order with ID {order_id} status updated to {status}."}

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add New Pizza
@router.post("/pizzas/", response_model=PizzaCreate, dependencies=[Depends(get_current_admin)])
async def create_pizza(pizza: PizzaCreate, db: Session = Depends(get_db)):
    new_pizza = Pizza(**pizza.dict())
    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)
    return new_pizza

# 2. Update Pizza Details
@router.put("/pizzas/{pizza_id}", response_model=PizzaUpdate, dependencies=[Depends(get_current_admin)])
async def update_pizza(pizza_id: int, pizza: PizzaUpdate, db: Session = Depends(get_db)):
    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    for key, value in pizza.dict(exclude_unset=True).items():
        setattr(db_pizza, key, value)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza

# 3. Delete a Pizza
@router.delete("/pizzas/{pizza_id}", dependencies=[Depends(get_current_admin)])
async def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    db.delete(db_pizza)
    db.commit()
    return {"msg": f"Pizza with ID {pizza_id} deleted."}

# 4. Update Order Status
@router.put("/orders/{order_id}/status", response_model=OrderStatusUpdate, dependencies=[Depends(get_current_admin)])
async def update_order_status(order_id: int, order_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)
    return db_order