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
