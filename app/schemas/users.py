from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    is_active: bool = True
    is_customer: bool = True
    is_vendor: bool = False
    # BUG 33: Missing validation for username length and format
    # BUG 34: Missing validation for email domain


class UserCreate(UserBase):
    password: str
    # BUG 35: Missing password strength validation
    # BUG 36: Missing password confirmation field


class UserRead(UserBase):
    id: int
    # BUG 37: Missing password field in read schema (should be excluded)

    class Config:
        orm_mode = True


# BUG 38: Missing UserUpdate schema for partial updates
