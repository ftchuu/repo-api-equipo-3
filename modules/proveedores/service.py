from core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from fastapi import HTTPException

def _to_none_if_false(value):
    return None if value is False else value

def obtener_proveedores():
    uid, models = get_odoo_connection()

    try:
        purchase_orders = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            "purchase.order", "search_read",
            [[]],
            {"fields": ["partner_id"]}
        )

        proveedor_ids = list({
            po["partner_id"][0]
            for po in purchase_orders
            if po.get("partner_id")
        })

        if not proveedor_ids:
            return {"total": 0, "data": []}

        proveedores_raw = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            "res.partner", "search_read",
            [[("id", "in", proveedor_ids), ("active", "=", True)]],
            {
                "fields": ["id", "name", "vat", "email", "phone", "mobile"],
                "order": "name"
            }
        )

        proveedores = []
        for p in proveedores_raw:
            proveedores.append({
                "id": int(p["id"]),
                "name": str(p["name"]) if p.get("name") not in (False, None) else "",
                "vat": _to_none_if_false(p.get("vat")),
                "email": _to_none_if_false(p.get("email")),
                "phone": _to_none_if_false(p.get("phone")),
                "mobile": _to_none_if_false(p.get("mobile")),
            })

        return {"total": len(proveedores), "data": proveedores}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))