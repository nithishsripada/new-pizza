from fastapi import APIRouter, Depends, HTTPException
from schemas import CartItem, OrderCreate, CartAdd, CartItemResponse, CheckoutResponse, OrderResponse
from typing import List
from auth import get_current_active_user, get_current_customer
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cart, Pizza, Order, Payment


router = APIRouter()

@router.get("/pizzas/", response_model=List[dict], dependencies=[Depends(get_current_active_user)])
async def list_pizzas():
    # Placeholder to list all available pizzas
    return [{"id": 1, "name": "Meat pizza", "amount": 10.0, "availability": "Available"}]

@router.post("/cart/", response_model=CartItem, dependencies=[Depends(get_current_active_user)])
async def add_to_cart(item: CartItem):
    # Placeholder to add item to the cart
    return item

@router.delete("/cart/{item_id}", dependencies=[Depends(get_current_active_user)])
async def remove_from_cart(item_id: int):
    # Placeholder to remove item from the cart
    return {"msg": f"Item with ID {item_id} removed from cart."}

@router.post("/checkout/", response_model=OrderCreate, dependencies=[Depends(get_current_active_user)])
async def checkout():
    # Placeholder code to checkout cart and create order
    return {"order_id": 1, "status": "Pending"}

@router.get("/orders/", response_model=List[OrderCreate], dependencies=[Depends(get_current_active_user)])
async def view_orders():
    # Placeholder to list previous orders
    return [{"order_id": 1, "status": "Delivered", "description": "Order of Meat pizza"}]

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add Pizza to Cart
@router.post("/cart/", response_model=CartItemResponse, dependencies=[Depends(get_current_customer)])
async def add_to_cart(cart_add: CartAdd, db: Session = Depends(get_db), current_user=Depends(get_current_customer)):
    pizza = db.query(Pizza).filter(Pizza.id == cart_add.pizza_id).first()
    if not pizza or not pizza.availability:
        raise HTTPException(status_code=404, detail="Pizza not available")

    cart_item = Cart(user_id=current_user.id, pizza_id=cart_add.pizza_id, quantity=cart_add.quantity, total=pizza.amount * cart_add.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

# 2. View Cart Details
@router.get("/cart/", response_model=List[CartItemResponse], dependencies=[Depends(get_current_customer)])
async def view_cart(db: Session = Depends(get_db), current_user=Depends(get_current_customer)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    return cart_items

# 3. Clear Cart
@router.delete("/cart/clear", dependencies=[Depends(get_current_customer)])
async def clear_cart(db: Session = Depends(get_db), current_user=Depends(get_current_customer)):
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()
    return {"msg": "Cart cleared"}

# 4. Checkout and Create Order
@router.post("/cart/checkout", response_model=CheckoutResponse, dependencies=[Depends(get_current_customer)])
async def checkout_cart(db: Session = Depends(get_db), current_user=Depends(get_current_customer)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(item.total for item in cart_items)
    new_order = Order(customer_id=current_user.id, description="Pizza order", status="Pending", instructions="")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Optional: Simulate payment processing
    payment = Payment(customer_id=current_user.id, amount=total_amount)
    db.add(payment)
    db.commit()

    # Clear cart after checkout
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()

    return CheckoutResponse(order_id=new_order.id, total_amount=total_amount)

# 5. View Previous Orders
@router.get("/orders/", response_model=List[OrderResponse], dependencies=[Depends(get_current_customer)])
async def view_previous_orders(db: Session = Depends(get_db), current_user=Depends(get_current_customer)):
    orders = db.query(Order).filter(Order.customer_id == current_user.id).all()
    return orders