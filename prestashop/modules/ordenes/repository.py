from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException

def obtener_ordenes_repository():
    try:
        data = prestashop_get("orders")
        return data.get("orders", [])

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
