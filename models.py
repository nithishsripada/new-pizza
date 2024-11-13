from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String)
       mobile = Column(String)
       address = Column(String)
       email = Column(String, unique=True, index=True)
       password = Column(String)
       role = Column(String)  # e.g., "customer", "admin", "delivery_partner"

class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    type = Column(String)
    amount = Column(Float)
    availability = Column(Boolean, default=True)

class Cart(Base):
       __tablename__ = "carts"
       id = Column(Integer, primary_key=True, index=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       pizza_id = Column(Integer, ForeignKey("pizzas.id"))
       quantity = Column(Integer)
       total = Column(Float)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("users.id"))
    order_number = Column(String)
    status = Column(String)
    instructions = Column(String, nullable=True)

class Delivery(Base):
       __tablename__ = "deliveries"
       id = Column(Integer, primary_key=True, index=True)
       user_id = Column(Integer, ForeignKey("users.id"))  # Delivery Partner
       order_id = Column(Integer, ForeignKey("orders.id"))
       start_time = Column(String)
       end_time = Column(String)
       status = Column(String)
       comment = Column(String, nullable=True)

class Payment(Base):
       __tablename__ = "payments"
       id = Column(Integer, primary_key=True, index=True)
       customer_id = Column(Integer, ForeignKey("users.id"))
       amount = Column(Float)
       date = Column(String)