from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException

def obtener_clientes():
    try:
        data = prestashop_get("customers")
        clientes = data.get("customers", [])

        resultado = []
        for cliente in clientes:
            resultado.append({
                "id": cliente.get("id"),
                "firstname": cliente.get("firstname"),
                "lastname": cliente.get("lastname"),
                "email": cliente.get("email")
            })
        return resultado

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))