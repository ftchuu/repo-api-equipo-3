from fastapi import APIRouter
from .service import (
    crear_producto_por_referencia,
    buscar_producto_por_referencia,
    crear_productos_masivamente,
)
from .schemas import Producto, ProductoReferencia, ProductosMasivos

router = APIRouter()


# colocar la ruta fija antes de la dinámica para que FastAPI no la
# interprete como un valor de `reference` 
@router.get("/masivo", response_model=ProductosMasivos)
def sincronizar_masivo():
    """Importa en bloque los productos de Odoo a PrestaShop."""
    return crear_productos_masivamente()


@router.get("/{reference}", response_model=Producto)
def obtener_por_referencia(reference: str):
    return buscar_producto_por_referencia(reference)


@router.post("/")
def crear_por_referencia(body: ProductoReferencia):
    return crear_producto_por_referencia(body.reference)

