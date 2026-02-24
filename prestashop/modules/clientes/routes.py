from fastapi import APIRouter
from .service import listar_clientes
from .schemas import ClienteLista

router = APIRouter()

@router.get("/", response_model=ClienteLista)
def obtener_clientes():
    return listar_clientes()