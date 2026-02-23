from core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from fastapi import HTTPException


def obtener_productos():
	uid, models = get_odoo_connection()

	try:
		productos = models.execute_kw(
			ODOO_DB, uid, ODOO_PASSWORD,
			"product.product", "search_read",
			[[]],
			{
				"fields": ["id", "name", "default_code", "list_price", "type", "categ_id"],
				"order": "name"
			}
		)

		# Normalizar datos para que coincidan con los esquemas Pydantic
		for prod in productos:
			# Algunos registros pueden tener `default_code` como False; convertir a None
			dc = prod.get("default_code")
			if dc is False:
				prod["default_code"] = None
			elif dc is not None and not isinstance(dc, str):
				prod["default_code"] = str(dc)

		return {"total": len(productos), "data": productos}

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

