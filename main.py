from fastapi import FastAPI
from routes import customers, food, orders, staff

app = FastAPI()

# Register routes
app.include_router(customers.router)
app.include_router(food.router)
app.include_router(orders.router)
app.include_router(staff.router)  # Register the staff routes here
