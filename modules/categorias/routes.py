from fastapi import APIRouter
from .service import obtener_categorias
from .schemas import CategoriaResponse

router = APIRouter()

@router.get("/", response_model=CategoriaResponse)
def listar_categorias():
    return obtener_categorias()