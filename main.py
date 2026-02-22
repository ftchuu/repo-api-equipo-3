from fastapi import FastAPI
from modules.productos.routes import router as products_router

app = FastAPI(title="API")

app.include_router(products_router, prefix="/api/productos", tags=["Productos"])