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
    


class UserCreate(UserBase):
    password: str
   


class UserRead(UserBase):
    id: int
    

    class Config:
        orm_mode = True



