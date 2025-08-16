from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class User(Base):
    __tablename__ = "users_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    first_name = Column(String(150), default="")
    last_name = Column(String(150), default="")
    is_active = Column(Boolean, default=True)
    is_customer = Column(Boolean, default=True)
    is_vendor = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # BUG 23: Missing password field in model but used in schema

    reviews = relationship("ProductReview", back_populates="user")
    products = relationship("Product", back_populates="vendor")
    orders = relationship("Order", back_populates="customer")


class Category(Base):
    __tablename__ = "products_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, default="")
    slug = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # BUG 24: Missing parent_id for hierarchical categories

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products_product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("products_category.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    sku = Column(String(50), unique=True)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # BUG 25: Missing check constraint for positive price
    # BUG 26: Missing check constraint for non-negative stock

    category = relationship("Category", back_populates="products")
    vendor = relationship("User", back_populates="products")
    reviews = relationship("ProductReview", back_populates="product")


class ProductReview(Base):
    __tablename__ = "products_productreview"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products_product.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # BUG 27: Missing check constraint for rating range (1-5)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Order(Base):
    __tablename__ = "orders_order"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    status = Column(String(20), default="pending")
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    subtotal = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    shipping_cost = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # BUG 28: Missing check constraint for valid status values
    # BUG 29: Missing check constraint for positive amounts

    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    status_history = relationship("OrderStatus", back_populates="order")


class OrderItem(Base):
    __tablename__ = "orders_orderitem"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products_product.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # BUG 30: Missing check constraint for positive quantity
    # BUG 31: Missing check constraint for positive prices

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class OrderStatus(Base):
    __tablename__ = "orders_orderstatus"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=False)
    status = Column(String(20), nullable=False)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users_user.id"))
    # BUG 32: Missing check constraint for valid status values

    order = relationship("Order", back_populates="status_history")
