from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import OrderSchema, OrderCreateSchema, OrderStatusUpdateSchema
from app.database import get_db
from app.crud_orders import create_order, get_orders, get_order, update_order_status

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@order_router.post(
        "/", 
        response_model=OrderSchema,
        )
async def create_order_endpoint(
    order_data: OrderCreateSchema, 
    db: AsyncSession = Depends(get_db),
    ):
    return await create_order(
        db=db, 
        order_data=order_data,
        )

@order_router.get(
        "/", 
        response_model=List[OrderSchema],
        )
async def read_orders_endpoint(
    db: AsyncSession = Depends(get_db),
    ):
    return await get_orders(db=db,)

@order_router.get(
        "/{order_id}", 
        response_model=OrderSchema,
        )
async def read_order_endpoint(
    order_id: int, 
    db: AsyncSession = Depends(get_db),
    ):
    order = await get_order(
        db=db, 
        order_id=order_id,
        )
    if order is None:
        raise HTTPException(
            status_code=404, 
            detail="Order not found",
            )
    return order

@order_router.patch(
        "/{order_id}/status", 
        response_model=OrderSchema,
        )
async def update_order_status_endpoint(
    order_id: int, 
    status: OrderStatusUpdateSchema, 
    db: AsyncSession = Depends(get_db),
    ):
    return await update_order_status(
        db=db, 
        order_id=order_id, 
        new_status=status,
        )
