from fastapi import FastAPI
from modules.productos.routes import router as productos_router
from modules.categorias.routes import router as categorias_router
from modules.stock.routes import router as stock_router

app = FastAPI(title="API")

# Obtener productos
app.include_router(productos_router, prefix="/api/productos", tags=["Productos"])

# Obtener categorías de productos
app.include_router(categorias_router, prefix="/api/categorias", tags=["Categorías"])

#Obtener stock de productos
app.include_router(stock_router, prefix="/api/stock", tags=["Stock"])