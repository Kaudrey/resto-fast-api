from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from models.customer import Customer
from database import get_db
from typing import List
from utils.password_utils import hash_password
from fastapi import Query
from fastapi import FastAPI, Query, Depends, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Hash the password before saving
    hashed_password = hash_password(customer.password)
    new_customer = Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        phone_number=customer.phone_number,
        password=hashed_password
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[CustomerOut])
def get_customers(
    request: Request,  # Added to support rendering
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    total_customers = db.query(Customer).count()
    page_number = (skip // limit) + 1
    total_pages = (total_customers + limit - 1) // limit

    # Render the template for the browser
    return templates.TemplateResponse(
        "customers.html",
        {
            "request": request,
            "customers": customers,
            "page_number": page_number,
            "total_pages": total_pages,
            "limit": limit
        }
    )

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted successfully"}
