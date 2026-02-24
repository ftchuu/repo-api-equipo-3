from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException

def obtener_proveedores():
    try:
        data = prestashop_get("suppliers")
        proveedores = data.get("suppliers", [])

        resultado = []
        for proveedor in proveedores:
            resultado.append({
                "id": proveedor.get("id"),
                "name": proveedor.get("name")
            })
        return resultado

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))