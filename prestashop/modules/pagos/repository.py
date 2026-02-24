from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException

def obtener_pagos():
    try:
        data = prestashop_get("order_payments")
        pagos = data if isinstance(data, list) else data.get("order_payments", [])

        resultado = []
        for pago in pagos:
            resultado.append({
                "id": pago.get("id"),
                "amount": pago.get("amount"),
                "payment_method": pago.get("payment_method"),
                "date_add": pago.get("date_add")
            })
        return resultado

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))