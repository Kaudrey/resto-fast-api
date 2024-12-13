from sqlalchemy import Column, Integer, Float, String, ForeignKey
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    total_price = Column(Float)
    customer_id = Column(Integer, ForeignKey('customers.id'))  # ForeignKey to Customer
    created_at = Column(DateTime, default=datetime.utcnow, nullable= False)

    customer = relationship("Customer", backref="orders", uselist=False)
    items = relationship("OrderItem", backref="order")  # Relationship with OrderItem

    def __repr__(self):
        return f"<Order(id={self.id}, quantity={self.quantity}, total_price={self.total_price})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    food_item_id = Column(Integer, ForeignKey("food_items.id"))
    quantity = Column(Integer)
    price = Column(Float)  # Total price for this item (quantity * item price)

    food_item = relationship("FoodItem", back_populates="order_items") 