from pydantic import BaseModel
from typing import Optional, List


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total_price: float


class OrderBase(BaseModel):
    order_number: Optional[str] = None
    customer_id: int
    status: Optional[str] = "pending"
    shipping_address: str
    billing_address: str
    subtotal: float = 0
    tax_amount: float = 0
    shipping_cost: float = 0
    total_amount: float = 0


class OrderRead(OrderBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        from_attributes = True
