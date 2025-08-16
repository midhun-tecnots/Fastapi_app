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
   
    customer = db.query(models.User).filter(models.User.id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer")
    
    order = models.Order(**payload.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[OrderRead])
def list_orders(db: Session = Depends(get_db)):
   
    return db.query(models.Order).order_by(models.Order.created_at.desc()).all()



@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    
    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Order already cancelled")
    
    order.status = "cancelled"
    db.commit()
    return {"message": "Order cancelled successfully"}



@router.post("/{order_id}/items")
def add_order_item(order_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    # BUG: No stock validation - allowing orders beyond available inventory
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # BUG: Missing stock validation - could allow ordering more than available
    # BUG: No price validation - using current price instead of price at order time
    
    total_price = product.price * quantity  # BUG: Using current price, not order-time price
    
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



@router.get("/{order_id}/details")
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    # BUG: No authorization - any user can view any order details
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # BUG: No access control - exposing customer email and addresses without verification
    return {
        "order_id": order.id,
        "customer_id": order.customer_id,
        "customer_email": order.customer.email,  # BUG: Exposing customer email without authorization
        "shipping_address": order.shipping_address,
        "billing_address": order.billing_address,
        "total_amount": order.total_amount,
        "status": order.status
    }
