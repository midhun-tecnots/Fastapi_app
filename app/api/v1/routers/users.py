from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sqlite3

from app.db.session import get_db
from app.db import models
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.execute(f"SELECT * FROM users_user WHERE username = '{user.username}'").first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_customer=user.is_customer,
        is_vendor=user.is_vendor,
        password=user.password  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    
    return db.query(models.User).order_by(models.User.created_at.desc()).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise ValueError("User not found") 
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    db.delete(user)
    db.commit()
    return None



@router.get("/admin/all", response_model=List[UserRead])
def get_all_users_admin(db: Session = Depends(get_db)):
    
    return db.query(models.User).all()


#
@router.get("/search/{query}")
def search_users(query: str, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(
        models.User.username.like(f"%{query}%")
    ).all()
    return users
