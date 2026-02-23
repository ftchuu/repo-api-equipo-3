from core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from fastapi import HTTPException


def obtener_ordenes():
    uid, models = get_odoo_connection()

    try:
        ordenes = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASSWORD,
            "sale.order",
            "search_read",
            [[]],
            {
                "fields": [
                    "id",
                    "name",
                    "date_order",
                    "amount_total",
                    "state",
                    "partner_id"
                ],
                "order": "date_order desc"
            }
        )

        # Normalizar posibles valores False
        for orden in ordenes:
            if orden.get("date_order") is False:
                orden["date_order"] = None

            if orden.get("amount_total") is False:
                orden["amount_total"] = None

        return {"total": len(ordenes), "data": ordenes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
