from pydantic import BaseModel
from typing import List
from datetime import datetime

# Schema to represent each item in the order
class OrderItemBase(BaseModel):
    food_item_id: int  # The ID of the food item
    quantity: int  # The quantity of the food item

    class Config:
        orm_mode = True  # This tells Pydantic to work with SQLAlchemy models


# Request body schema for creating an order
class OrderCreate(BaseModel):
    customer_id: int  # The ID of the customer
    items: List[OrderItemBase]  # A list of order items with food_item_id and quantity
    total_price: float  # The total price of the order (this will be calculated in the backend)

    class Config:
        orm_mode = True  # This tells Pydantic to work with SQLAlchemy models


# Response body schema for retrieving an order
class OrderOut(BaseModel):
    id: int  # The ID of the order
    customer_id: int  # The ID of the customer
    items: List[OrderItemBase]  # A list of order items
    total_price: float  # The total price of the order
    created_at: datetime  # The creation time of the order

    class Config:
        from_attributes = True  # This tells Pydantic to work with SQLAlchemy models
