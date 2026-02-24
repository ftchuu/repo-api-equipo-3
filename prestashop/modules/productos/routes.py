from fastapi import APIRouter
from .service import listar_productos
from .schemas import ProductoLista

router = APIRouter()

@router.get("/", response_model=ProductoLista)
def obtener_productos():
    return listar_productos()


@router.get("/sku/{sku}")
def obtener_producto_sku(sku: str):
    from .service import buscar_producto_por_sku
    return buscar_producto_por_sku(sku)