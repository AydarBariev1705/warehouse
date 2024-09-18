from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models import Product
from app.schemas import ProductCreateSchema, ProductUpdateSchema

async def create_product(
        db: AsyncSession, 
        product: ProductCreateSchema,
        ):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(
        db: AsyncSession, 
        product_id: int,
        ):
    product = await db.get(
        Product, 
        product_id,
        )
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found",
            )
    return product

async def update_product(
        db: AsyncSession, 
        product_id: int, 
        product_data: ProductUpdateSchema,
        ):
    product = await db.get(
        Product, 
        product_id,
        )
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found",
            )
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(
            product, 
            key, 
            value,
            )
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(
        db: AsyncSession, 
        product_id: int,
        ):
    product = await db.get(
        Product, 
        product_id,
        )
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Product not found",
            )
    await db.delete(product)
    await db.commit()
