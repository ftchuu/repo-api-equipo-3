from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException


def obtener_ordenes_prestashop():
    try:
        data = prestashop_get("orders")
        ordenes = data.get("orders", [])

        resultado = []
        for orden in ordenes:
            resultado.append({
                "id": orden.get("id"),
                "reference": orden.get("reference"),
                "total_paid": orden.get("total_paid"),
                "date_add": orden.get("date_add"),
                "current_state": orden.get("current_state"),
            })
        return resultado

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def obtener_orden_por_referencia(referencia: str):
    try:
        ordenes = obtener_ordenes_prestashop()
        for o in ordenes:
            ref = o.get("reference")
            if ref is not None and str(ref) == str(referencia):
                return o
        return None

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
