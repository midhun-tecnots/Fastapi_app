from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.db.session import get_db
from app.db import models
from app.schemas.orders import OrderRead, OrderBase

router = APIRouter(prefix="/orders")


@router.post("/", response_model=OrderRead, status_code=201)
def create_order(payload: OrderBase, db: Session = Depends(get_db)):
    # BUG 16: Missing order number generation
    customer = db.query(models.User).filter(models.User.id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer")
    
    # BUG 17: Missing stock validation before creating order
    # BUG 18: Missing total amount calculation
    order = models.Order(**payload.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    # BUG 19: Missing customer authorization - users can see all orders
    return db.query(models.Order).order_by(models.Order.created_at.desc()).all()


# BUG 20: New endpoint with race condition vulnerability
@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # BUG: Race condition - multiple requests could cancel the same order
    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Order already cancelled")
    
    order.status = "cancelled"
    db.commit()
    return {"message": "Order cancelled successfully"}


# BUG 21: Endpoint with potential integer overflow
@router.post("/{order_id}/items")
def add_order_item(order_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    # BUG: No validation for quantity limits
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # BUG: No stock validation
    # BUG: Potential integer overflow in price calculations
    total_price = product.price * quantity  # Could overflow for large quantities
    
    order_item = models.OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=product.price,
        total_price=total_price
    )
    db.add(order_item)
    db.commit()
    return order_item


# BUG 22: Endpoint with information disclosure
@router.get("/{order_id}/details")
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # BUG: Exposing sensitive customer information without authorization
    return {
        "order_id": order.id,
        "customer_id": order.customer_id,
        "customer_email": order.customer.email,  # Exposing customer email!
        "shipping_address": order.shipping_address,
        "billing_address": order.billing_address,
        "total_amount": order.total_amount,
        "status": order.status
    }
