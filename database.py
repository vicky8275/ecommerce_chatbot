from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String(50))
    items = Column(Text)
    date = Column(DateTime, default=datetime.now)
    shipping_address = Column(Text)

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    issue_description = Column(Text)
    date = Column(DateTime, default=datetime.now)
    status = Column(String(50), default='open')

# Database initialization
engine = create_engine('sqlite:///ecommerce.db', echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Seed sample data
def seed_database():
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(User).count() > 0:
        db.close()
        return
    
    # Sample users
    users = [
        User(user_id=1, name="John Doe", email="john@example.com"),
        User(user_id=2, name="Jane Smith", email="jane@example.com")
    ]
    
    # Sample orders
    orders = [
        Order(order_id=12345, user_id=1, status="shipped", 
              items="Running Shoes - Size 10", 
              shipping_address="123 Main St, City, State"),
        Order(order_id=12346, user_id=1, status="delivered",
              items="Laptop Bag",
              shipping_address="123 Main St, City, State"),
        Order(order_id=12347, user_id=2, status="processing",
              items="Wireless Headphones",
              shipping_address="456 Oak Ave, Town, State")
    ]
    
    db.add_all(users + orders)
    db.commit()
    db.close()
    print("✓ Database seeded with sample data")