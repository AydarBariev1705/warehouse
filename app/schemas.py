from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from app.enums import OrderStatus

class ProductBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    quantity: int

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(ProductBaseSchema):
    pass

class ProductSchema(ProductBaseSchema):
    id: int

    class Config:
        orm_mode = True

class OrderBaseSchema(BaseModel):
    status: OrderStatus

class OrderItemBaseSchema(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreateSchema(OrderItemBaseSchema):
    pass

class OrderItemSchema(OrderItemBaseSchema):
    id: int
    product: ProductSchema  

    class Config:
        orm_mode = True

class OrderCreateSchema(BaseModel):
    items: List[OrderItemCreateSchema]

class OrderStatusUpdateSchema(BaseModel):
    status: OrderStatus

class OrderSchema(OrderBaseSchema):
    id: int
    created_at: datetime
    items: List[OrderItemSchema]

    class Config:
        orm_mode = True
