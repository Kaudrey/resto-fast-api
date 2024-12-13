from faker import Faker
from sqlalchemy.orm import Session
from models.customer import Customer
from database import get_db
from utils.password_utils import hash_password
from sqlalchemy.exc import IntegrityError

# Initialize Faker
fake = Faker()

# Function to create a fake customer
def create_fake_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.unique.email()
    phone_number = fake.phone_number()[:15]
    password = fake.password(length=8)
    hashed_password = hash_password(password)
    
    # Return a dictionary for Customer data
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "password": hashed_password,
    }

# Function to insert 500,000 fake customers into the database
def insert_fake_customers(db: Session, num_customers: int = 500000):
    customers_to_insert = []
    inserted_count = 0  # Counter for successfully inserted customers
    
    for _ in range(num_customers):
        fake_customer_data = create_fake_customer()
        fake_customer = Customer(**fake_customer_data)  # Unpack the dictionary into the Customer object
        
        # Try to insert the customer individually
        try:
            db.add(fake_customer)
            db.commit()  # Commit immediately after adding each customer
            inserted_count += 1
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction in case of an error (e.g., duplicate email)
            print(f"Duplicate or error inserting customer: {fake_customer_data['email']}")
            continue  # Skip to the next iteration
    
    print(f"Successfully inserted {inserted_count} customers.")

# Main function to run the script
def main():
    db = next(get_db())  # Assuming get_db() returns a session
    insert_fake_customers(db)

if __name__ == "__main__":
    main()
