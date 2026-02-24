from fastapi import HTTPException
from .repository import obtener_ordenes_prestashop, obtener_orden_por_referencia


def listar_ordenes():
    ordenes = obtener_ordenes_prestashop()
    return {"total": len(ordenes), "data": ordenes}


def buscar_orden_por_referencia(referencia: str):
    orden = obtener_orden_por_referencia(referencia)
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada en PrestaShop")
    return orden
