from core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from fastapi import HTTPException

def obtener_stock_productos():
    uid, models = get_odoo_connection()

    try:
        productos = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            "product.product", "search_read",
            [[("type", "=", "product")]], 
            {
                "fields": ["id", "name", "default_code", "qty_available"], 
                "order": "name"
            }
        )
        # Se filtra por type="product" para traer solo productos almacenables

        return {"total": len(productos), "data": productos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))