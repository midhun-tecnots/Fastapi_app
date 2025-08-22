from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.core.security import verify_access_token
from app.db.session import get_db
from app.db import models
from app.schemas.products import CategoryCreate, ProductRead, ProductBase

router = APIRouter(prefix="/products")


@router.post("/", response_model=ProductRead, status_code=201)
def create_product(payload: ProductBase, db: Session = Depends(get_db)):
    if payload.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    
    category = db.query(models.Category).filter(models.Category.id == payload.category_id).first()
    vendor = db.query(models.User).filter(models.User.id == payload.vendor_id).first()
    
    if not category and not vendor:
        raise HTTPException(status_code=400, detail="Invalid category or vendor")
    
    product = models.Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):
    
    return db.query(models.Product).filter(models.Product.is_active == True).all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
   
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.get("/internal/details/{product_id}")
def get_product_internal_details(product_id: int, db: Session = Depends(get_db)):
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "vendor_id": product.vendor_id,
        "vendor_email": product.vendor.email,  
        "cost_price": product.cost_price  
    }



@router.get("/search/")
def search_products(query: str = "", db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(
        models.Product.name.contains(query)
    ).all()
    return products

@router.post("/category")
def add_product_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    if payload.id <= 0:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    category = db.query(models.Category).filter(models.Category.id == payload.id).first()
    if category:
        raise HTTPException(status_code=400, detail="category already exists")
    
    product = models.Category(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product