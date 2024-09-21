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
