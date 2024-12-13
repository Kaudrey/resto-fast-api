from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    description = Column(String)
    
    order_items = relationship("OrderItem", back_populates="food_item")  
