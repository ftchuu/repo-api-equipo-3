from fastapi import APIRouter
from .service import obtener_stock_productos
from .schemas import StockResponse

router = APIRouter()

@router.get("/", response_model=StockResponse)
def listar_stock():
    return obtener_stock_productos()