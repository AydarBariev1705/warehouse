from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from app.database import get_db
from app.crud_products import create_product, get_products, get_product, update_product, delete_product

product_router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@product_router.post(
        "/", 
        response_model=ProductSchema,
        )
async def create_product_endpoint(
    product: ProductCreateSchema, 
    db: AsyncSession = Depends(get_db),
    ):
    return await create_product(
        db=db, 
        product=product,
        )

@product_router.get(
        "/", 
        response_model=List[ProductSchema],
        )
async def read_products_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_products(db=db,)

@product_router.get(
        "/{product_id}", 
        response_model=ProductSchema,
        )
async def read_product_endpoint(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    ):
    product = await get_product(
        db=db, 
        product_id=product_id,
        )
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail="Product not found",
            )
    return product

@product_router.put(
        "/{product_id}", 
        response_model=ProductSchema,
        )
async def update_product_endpoint(
    product_id: int, 
    product: ProductUpdateSchema, 
    db: AsyncSession = Depends(get_db),
    ):
    return await update_product(
        db=db, 
        product_id=product_id, 
        product_data=product,
        )

@product_router.delete("/{product_id}")
async def delete_product_endpoint(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    ):
    await delete_product(
        db=db, 
        product_id=product_id,
        )
    return {
        "detail": f"Product {product_id} deleted",
        }
