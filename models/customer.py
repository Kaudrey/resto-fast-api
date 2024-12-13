from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# SQLAlchemy model for Customer
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    balance = Column(Integer, default=0)
    password = Column(String)  # Add the password field for storing the hashed password

# Pydantic schemas for Customer
class CustomerBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: str = Field(..., max_length=15)

class CustomerCreate(CustomerBase):
    password: str = Field(..., min_length=6)  # Ensuring password field is required on creation

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=15)
    password: Optional[str] = None  # Optional password for updates if needed

class CustomerOut(CustomerBase):
    id: int
    balance: int

    class Config:
        orm_mode = True
