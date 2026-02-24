from fastapi import FastAPI

# ODOO IMPORTS
from modules.productos.routes import router as productos_router
from modules.categorias.routes import router as categorias_router
from modules.stock.routes import router as stock_router
from modules.proveedores.routes import router as proveedores_router
from modules.ordenes.routes import router as ordenes_router

# PRESTASHOP IMPORTS
from prestashop.modules.clientes.routes import router as clientes_router
from prestashop.modules.productos.routes import router as prestashop_productos_router
from prestashop.modules.proveedores.routes import router as proveedores_prestashop_router
from prestashop.modules.orden_referencia.routes import router as orden_ref_router

app = FastAPI(title="API")

# ODOO ENDPOINTS

app.include_router(productos_router, prefix="/api/odoo/productos", tags=["Productos"])
app.include_router(categorias_router, prefix="/odoo/categoria", tags=["Categoria"])
app.include_router(stock_router, prefix="/api/stock", tags=["Stock"])
app.include_router(proveedores_router, prefix="/api/proveedores", tags=["Proveedores"])
app.include_router(ordenes_router, prefix="/ordenes", tags=["Ordenes"])

# PRESTASHOP ENDPOINTS

app.include_router(clientes_router, prefix="/prestashop/clientes", tags=["Clientes"])
app.include_router(prestashop_productos_router, prefix="/api/prestashop/productos", tags=["Productos"])
app.include_router(proveedores_prestashop_router, prefix="/api/prestashop/proveedores", tags=["PrestaShop Proveedores"])
app.include_router(orden_ref_router, prefix="/api/prestashop/orden-referencia", tags=["Ordenes Prestashop"])