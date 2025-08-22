from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = ""
    slug: Optional[str] = None
    is_active: bool = True


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    category_id: int
    vendor_id: int
    sku: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True
