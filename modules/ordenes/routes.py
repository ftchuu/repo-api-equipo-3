from fastapi import APIRouter
from .service import obtener_ordenes
from .schemas import OrdenesResponse

router = APIRouter()


@router.get("/", response_model=OrdenesResponse)
def listar_ordenes():
    return obtener_ordenes()
