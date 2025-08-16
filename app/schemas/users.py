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
    # BUG: Missing password validation - no length or complexity requirements
    


class UserCreate(UserBase):
    password: str
    # BUG: No password validation - should have minimum length and complexity requirements
   


class UserRead(UserBase):
    id: int
    

    class Config:
        orm_mode = True



