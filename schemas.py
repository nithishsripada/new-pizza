from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
       name: str
       email: str
       password: str
       role: str  # "customer", "admin", or "delivery_partner"

class PizzaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    amount: float
    availability: bool

class CartItem(BaseModel):
       pizza_id: int
       quantity: int

class OrderCreate(BaseModel):
       customer_id: int
       description: str
       status: str
       instructions: Optional[str] = None

class PizzaUpdate(BaseModel):
    description: Optional[str]
    type: Optional[str]
    amount: Optional[float]
    availability: Optional[bool]

class OrderStatusUpdate(BaseModel):
    status: str

class CartAdd(BaseModel):
    pizza_id: int
    quantity: int

class CartItemResponse(BaseModel):
    pizza_id: int
    quantity: int
    total: float

class CheckoutResponse(BaseModel):
    order_id: int
    total_amount: float

class OrderResponse(BaseModel):
    id: int
    description: str
    status: str
    instructions: Optional[str] = None

class DeliveryStatusUpdate(BaseModel):
    status: str
    comment: Optional[str] = None