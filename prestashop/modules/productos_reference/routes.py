from fastapi import APIRouter
from .service import crear_producto_por_referencia, buscar_producto_por_referencia
from .schemas import Producto, ProductoReferencia

router = APIRouter()


@router.get("/{reference}", response_model=Producto)
def obtener_por_referencia(reference: str):
    return buscar_producto_por_referencia(reference)


@router.post("/")
def crear_por_referencia(body: ProductoReferencia):
    return crear_producto_por_referencia(body.reference)
