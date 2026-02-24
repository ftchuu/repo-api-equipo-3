from fastapi import APIRouter
from .service import listar_ordenes
from .schemas import OrdenReferenciaLista

router = APIRouter()

@router.get("/", response_model=OrdenReferenciaLista)
def obtener_ordenes():
    return listar_ordenes()


@router.get("/reference/{reference}")
def obtener_orden(reference: str):
    from .service import buscar_orden_por_referencia
    return buscar_orden_por_referencia(reference)
