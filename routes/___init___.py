from fastapi import APIRouter
from .staff import router as staff_router
from .customers import router as customer_router
from .food import router as food_router
from .orders import router as order_router

router = APIRouter()
router.include_router(staff_router, prefix="/staff", tags=["Staff"])
router.include_router(customer_router, prefix="/customers", tags=["Customers"])
router.include_router(food_router, prefix="/food", tags=["Food Items"])
router.include_router(order_router, prefix="/orders", tags=["Orders"])
