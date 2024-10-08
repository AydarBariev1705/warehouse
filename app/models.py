from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums import OrderStatus


class Product(Base):
    __tablename__ = "products"
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    name = Column(
        String, 
        index=True,
        )
    description = Column(String)
    price = Column(
        DECIMAL(
            precision=10, 
            scale=2,
            ),
            )
    quantity = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    created_at = Column(
        DateTime, 
        default=datetime.utcnow,
        )
    status = Column(
        Enum(OrderStatus), 
        default=OrderStatus.in_progress,
        )

    items = relationship(
        "OrderItem", 
        back_populates="order",
        )

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    order_id = Column(
        Integer, 
        ForeignKey("orders.id"),
        )
    product_id = Column(
        Integer, 
        ForeignKey("products.id"),
        )
    quantity = Column(Integer)

    order = relationship(
        "Order", 
        back_populates="items",
        )
    product = relationship("Product")
