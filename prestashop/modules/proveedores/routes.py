from fastapi import APIRouter
from .service import listar_proveedores
from .schemas import ProveedorLista

router = APIRouter()

@router.get("/", response_model=ProveedorLista)
def obtener_proveedores():
    return listar_proveedores()