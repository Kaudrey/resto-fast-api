from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: str = Field(..., max_length=15)

class CustomerCreate(CustomerBase):
    password: str = Field(..., min_length=6)

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=15)

class CustomerOut(CustomerBase):
    id: int
    balance: float

    class Config:
        from_attributes = True
