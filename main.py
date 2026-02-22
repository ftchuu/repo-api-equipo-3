from fastapi import FastAPI
from modules.productos.routes import router as productos_router

app = FastAPI(title="API")

app.include_router(productos_router, prefix="/api/productos", tags=["Productos"])