from fastapi import FastAPI

from app.order_router import order_router
from app.product_router import product_router
from app.database import init_db



app = FastAPI()
app.include_router(product_router)
app.include_router(order_router)

@app.on_event("startup")
async def on_startup():
    await init_db()