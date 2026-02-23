from fastapi import APIRouter
from .service import obtener_proveedores
from .schemas import ProveedoresResponse

router = APIRouter()

@router.get("/", response_model=ProveedoresResponse)
def listar_proveedores():
    return obtener_proveedores()