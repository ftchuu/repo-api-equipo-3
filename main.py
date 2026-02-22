from fastapi import FastAPI
from modules.productos.routes import router as productos_router
from modules.categorias.routes import router as categorias_router

app = FastAPI(title="API")

# Obtener productos
app.include_router(productos_router, prefix="/api/productos", tags=["Productos"])

# Obtener categorías de productos
app.include_router(categorias_router, prefix="/api/categorias", tags=["Categorías"])