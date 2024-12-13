from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.staff import StaffCreate, StaffOut, StaffUpdate
from models.staff import Staff
from database import get_db
from typing import List
from utils.password_utils import hash_password

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=StaffOut)
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    # Hash the password before saving
    hashed_password = hash_password(staff.password)
    new_staff = Staff(
        first_name=staff.first_name,
        last_name=staff.last_name,
        email=staff.email,
        phone_number=staff.phone_number,
        password=hashed_password,
        role=staff.role  # e.g., admin, waiter, etc.
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

@router.get("/", response_model=List[StaffOut])
def get_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()

@router.get("/{staff_id}", response_model=StaffOut)
def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.put("/{staff_id}", response_model=StaffOut)
def update_staff(staff_id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    for key, value in staff.dict(exclude_unset=True).items():
        setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    db.delete(staff)
    db.commit()
    return {"detail": "Staff deleted successfully"}
