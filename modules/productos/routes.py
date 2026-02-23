from fastapi import APIRouter
from .service import obtener_productos
from .schemas import ProductosResponse

router = APIRouter()


@router.get("/", response_model=ProductosResponse)
def listar_productos():
	return obtener_productos()

