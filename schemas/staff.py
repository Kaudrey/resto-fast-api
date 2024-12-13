# schemas/staff.py
from pydantic import BaseModel
from typing import Optional

class StaffCreate(BaseModel):
    name: str
    role: str

    class Config:
        orm_mode = True

class StaffOut(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        orm_mode = True

class StaffUpdate(BaseModel):
    name: Optional[str] = None  # Use Optional from typing to indicate that this field can be None
    role: Optional[str] = None  # Same for the role field

    class Config:
        from_attributes = True
