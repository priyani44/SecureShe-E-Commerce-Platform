from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import stripe
import os
from models import Payment, User, Product, Category, Sale
from database import get_session
from email_utils import send_email

from datetime import date



app = FastAPI()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define data models
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

class Category(BaseModel):
    id: int
    name: str
    description: str

class Sale(BaseModel):
    id: int
    product_id: int
    user_id: int
    sale_date: str

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price: int

class Order(BaseModel):
    customer_name: str
    customer_email: str
    order_items: List[OrderItem]
    total_amount: int
    order_status: str = "pending"

class PaymentRequest(BaseModel):
    amount: int
    payment_method: str
    customer_name: str
    customer_email: str

class RefundRequest(BaseModel):
    order_id: str
    reason: str

# In-memory data storage (replace with a database in a real application)
users = []
products = []
categories = []
sales = []

@app.post("/register")
async def register_user(user: User):
    users.append(user)
    return JSONResponse(content={"message": "User registered successfully"}, status_code=201)

@app.post("/login")
async def login_user(username: str, password: str):
    for user in users:
        if user.username == username and user.password == password:
            return JSONResponse(content={"token": "dummy_token"}, status_code=200)
    return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)

@app.get("/products/")
async def get_products(token: str = Depends(oauth2_scheme)):
    return JSONResponse(content=products, status_code=200)

@app.get("/products/{category}")
async def get_products_by_category(category: str, token: str = Depends(oauth2_scheme)):
    category_products = [product for product in products if product.category == category]
    return JSONResponse(content=category_products, status_code=200)

@app.post("/products/")
async def create_product(product: Product, token: str = Depends(oauth2_scheme)):
    products.append(product)
    return JSONResponse(content={"message": "Product created successfully"}, status_code=201)

@app.post("/sales/")
async def make_sale(sale: Sale, token: str = Depends(oauth2_scheme)):
    sales.append(sale)
    return JSONResponse(content={"message": "Sale made successfully"}, status_code=201)

@app.get("/sales/")
async def get_sales(token: str = Depends(oauth2_scheme)):
    return JSONResponse(content=sales, status_code=200)

@app.post("/make_payment")
async def make_payment(payment_request: PaymentRequest):
    # Payment integration logic
    pass

@app.post("/place_order")
async def place_order(order: Order, db: Session = Depends(get_session)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    order_id = new_order.id
    send_email(order.customer_email, "Order Confirmation", "Your order has been placed successfully!")
    return JSONResponse(content={"order_id": order_id, "order_status": "pending"}, status_code=201)

@app.get("/get_order_status/{order_id}")
async def get_order_status(order_id: str, db: Session = Depends(get_session)):
    order_db = db.query(Order).filter_by(id=order_id).first()
    if order_db:
        return JSONResponse(content={"order_status": order_db.order_status}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/request_refund")
async def request_refund(refund_request: RefundRequest, db: Session = Depends(get_session)):
    order_db = db.query(Order).filter_by(id=refund_request.order_id).first()
    if order_db:
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        try:
            refund = stripe.Refund.create(charge=order_db.charge_id, amount=order_db.total_amount)
            order_db.order_status = "refunded"
            db.commit()
            return JSONResponse(content={"refund_status": "success"}, status_code=200)
        except stripe.error.StripeError:
            raise HTTPException(status_code=400, detail="Refund failed")
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/cancel_order/{order_id}")
async def cancel_order(order_id: str, db: Session = Depends(get_session)):
    order_db = db.query(Order).filter_by(id=order_id).first()
    if order_db:
        order_db.order_status = "cancelled"
        db.commit()
        return JSONResponse(content={"order_status": "cancelled"}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Order not found")
    
@app.post("/make_payment")
async def make_payment(payment_request: PaymentRequest, db: Session = Depends(get_session)):
    new_payment = Payment(
        amount=payment_request.amount,
        payment_method=payment_request.payment_method,
        customer_name=payment_request.customer_name,
        customer_email=payment_request.customer_email,
        payment_date=date.today()
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return JSONResponse(content={"message": "Payment recorded successfully", "payment_id": new_payment.id}, status_code=201)
model.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

class Product(Base):
    _tablename_ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

class Category(Base):
    _tablename_ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Sale(Base):
    _tablename_ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    sale_date = Column(Date)

    product = relationship("Product", back_populates="sales")
    user = relationship("User", back_populates="sales")

Product.sales = relationship("Sale", back_populates="product")
User.sales = relationship("Sale", back_populates="user")

class Payment(Base):
    _tablename_ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_method = Column(String)
    customer_name = Column(String)
    customer_email = Column(String)
    payment_date = Column(Date)
database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load database URL from environment variable or directly provide it here
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres-secureshe_owner:tYLwHE28IpvO@ep-wild-smoke-a1xjdvuf.ap-southeast-1.aws.neon.tech/postgres-secureshe?sslmode=require")

# Create engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()

def get_session():
    # Dependency that provides a SQLAlchemy session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
emai-utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email: str, subject: str, body: str):
    from_email = "twinksharma18@gmail.com"  # Replace with your email
    from_password = "nwve wwei msfx stvw"

    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
