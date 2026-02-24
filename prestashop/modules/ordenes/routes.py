from fastapi import APIRouter
from .service import obtener_ordenes_service
from .schemas import OrdenLista

router = APIRouter(tags=["Ordenes"])

@router.get("/", response_model=OrdenLista)
def obtener_ordenes():
    return obtener_ordenes_service()
