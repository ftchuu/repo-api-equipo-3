from fastapi import APIRouter
from .service import get_products

router = APIRouter()

@router.get("/")
def obtener_productos():
    return get_products()