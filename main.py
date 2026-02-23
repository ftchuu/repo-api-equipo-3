from fastapi import FastAPI
from modules.productos.routes import router as productos_router
from modules.categorias.routes import router as categorias_router
from modules.stock.routes import router as stock_router
from modules.proveedores.routes import router as proveedores_router
from modules.ordenes.routes import router as ordenes_router



app = FastAPI(title="API")

app.include_router(productos_router, prefix="/api/productos", tags=["Productos"])

app.include_router(categorias_router, prefix="/api/categoria", tags=["Categoria"])

app.include_router(stock_router, prefix="/api/stock", tags=["Stock"])

app.include_router(proveedores_router, prefix="/api/proveedores", tags=["Proveedores"])
app.include_router(ordenes_router, prefix="/ordenes", tags=["Ordenes"])
