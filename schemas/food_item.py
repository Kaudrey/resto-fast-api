from pydantic import BaseModel, Field
from typing import Optional

class FoodItemBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: float

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = None

class FoodItemOut(FoodItemBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
