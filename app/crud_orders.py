from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models import Order, OrderItem, Product
from app.schemas import OrderCreateSchema, OrderStatusUpdateSchema

async def create_order(
        db: AsyncSession, 
        order_data: OrderCreateSchema,
        ):
    async with db.begin(): 
        order_items = []
        total_quantity = {}

        for item in order_data.items:
            product = await db.get(
                Product, 
                item.product_id,
                )
            if product is None:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Product with id {item.product_id} not found",
                )
            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Not enough stock for product {product.name}",
                )

            total_quantity[product.id] = product.quantity - item.quantity
            order_item = OrderItem(
                product_id=item.product_id, 
                quantity=item.quantity,
            )
            order_items.append(order_item)

        new_order = Order(
            items=order_items,
        )
        db.add(new_order)

        for product_id, remaining_qty in total_quantity.items():
            product = await db.get(
                Product, 
                product_id,
                )
            if product is None:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Product with id {product_id} not found",
                )
            product.quantity = remaining_qty
            db.add(product)

        await db.commit()  

    
    async with db:  
        result = await db.execute(
            select(Order)
            .where(Order.id == new_order.id)
            .options(joinedload(Order.items)
                     .joinedload(OrderItem.product))
        )
        new_order = result.scalars().first()

    return new_order


async def get_orders(db: AsyncSession):
    async with db.begin(): 
        result = await db.execute(
            select(Order)
            .options(joinedload(Order.items)
                     .joinedload(OrderItem.product))  
            .distinct()
        )
        orders = result.scalars().unique().all()

        if not orders:
            raise HTTPException(
                status_code=404, 
                detail="No orders found",
                )

    return orders

async def get_order(
        db: AsyncSession, 
        order_id: int,
        ):
    async with db.begin(): 
        order = await db.get(
            Order, 
            order_id,
            )
        if not order:
            raise HTTPException(
                status_code=404, 
                detail="Order not found",
                )
        
        await db.execute(
            select(Order)
            .options(joinedload(Order.items)
                     .joinedload(OrderItem.product))
                     .filter(Order.id == order_id)
                     )

    return order

async def update_order_status(
        db: AsyncSession, 
        order_id: int, 
        new_status: OrderStatusUpdateSchema,
        ):
    async with db.begin():
        order = await db.get(
            Order, 
            order_id,
            )
        if not order:
            raise HTTPException(
                status_code=404, 
                detail="Order not found",
                )
        order.status = new_status.status
        await db.commit()
        
    async with db:  
        result = await db.execute(
            select(Order)
            .filter(Order.id == order_id)
            .options(joinedload(Order.items)
                     .joinedload(OrderItem.product))
        )
        updated_order = result.scalars().first()
    
    if updated_order is None:
        raise HTTPException(
            status_code=404, 
            detail="Order not found after commit",
            )
    
    return updated_order

