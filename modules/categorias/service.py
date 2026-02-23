from core.odoo import get_odoo_connection
from fastapi import HTTPException

def obtener_categorias():
    uid, models = get_odoo_connection()

    try:
        categorias = models.execute_kw(
            "tu_db", uid, "tu_password",
            "product.category", "search_read",
            [[]],
            {"fields": ["id", "name", "complete_name"], "order": "complete_name"}
        )

        return {"total": len(categorias), "data": categorias}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))