from fastapi import APIRouter
from .service import listar_pagos
from .schemas import PagoLista

router = APIRouter()
@router.get("/", response_model=PagoLista)
def obtener_pagos():
    return listar_pagos()