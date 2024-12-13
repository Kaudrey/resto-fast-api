from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderOut
from models.order import Order, OrderItem
from models.food_item import FoodItem
from database import get_db
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)  # Ensure response_model is OrderOut
def create_order(item: OrderCreate, db: Session = Depends(get_db)):
    # Fetch food items from the database
    food_items = []
    total_price = 0
    for order_item in item.items:
        food_item = db.query(FoodItem).filter(FoodItem.id == order_item.food_item_id).first()
        if not food_item:
            raise HTTPException(status_code=404, detail=f"Food item {order_item.food_item_id} not found")
        food_items.append(food_item)
        total_price += food_item.price * order_item.quantity

    # Create the order and the order items
    new_order = Order(customer_id=item.customer_id, total_price=total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for order_item in item.items:
        new_order_item = OrderItem(
            order_id=new_order.id,
            food_item_id=order_item.food_item_id,
            quantity=order_item.quantity,
            price=food_items[0].price * order_item.quantity,  # Assuming you calculate the price per item
        )
        db.add(new_order_item)

    db.commit()
    
    return new_order


@router.get("/", response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}
