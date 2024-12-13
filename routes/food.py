from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.food_item import FoodItemCreate, FoodItemOut, FoodItemUpdate
from models.food_item import FoodItem
from database import get_db
from typing import List

router = APIRouter(prefix="/food", tags=["Food Items"])

@router.post("/", response_model=FoodItemOut)
def create_food_item(food_item: FoodItemCreate, db: Session = Depends(get_db)):
    new_food_item = FoodItem(**food_item.dict())
    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)
    return new_food_item

@router.get("/", response_model=List[FoodItemOut])
def get_food_items(db: Session = Depends(get_db)):
    return db.query(FoodItem).all()

@router.get("/{food_item_id}", response_model=FoodItemOut)
def get_food_item(food_item_id: int, db: Session = Depends(get_db)):
    food_item = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")
    return food_item

@router.put("/{food_item_id}", response_model=FoodItemOut)
def update_food_item(food_item_id: int, food_item: FoodItemUpdate, db: Session = Depends(get_db)):
    db_food_item = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
    if not db_food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    for key, value in food_item.dict(exclude_unset=True).items():
        setattr(db_food_item, key, value)

    db.commit()
    db.refresh(db_food_item)
    return db_food_item

@router.delete("/{food_item_id}")
def delete_food_item(food_item_id: int, db: Session = Depends(get_db)):
    food_item = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")
    db.delete(food_item)
    db.commit()
    return {"detail": "Food item deleted successfully"}
