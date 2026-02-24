from prestashop.core.prestashop_client import prestashop_get
from fastapi import HTTPException


def obtener_productos_prestashop():
	try:
		data = prestashop_get("products")
		productos = data.get("products", [])

		resultado = []
		for producto in productos:
			pid = producto.get("id")

			nombre = None
			name_field = producto.get("name")
			if isinstance(name_field, list):
				if len(name_field) > 0:
					first = name_field[0]
					if isinstance(first, dict):
						nombre = first.get("value") or first.get("#text") or None
					else:
						nombre = str(first)
			elif isinstance(name_field, dict):
				lang = name_field.get("language")
				if isinstance(lang, list) and len(lang) > 0:
					first = lang[0]
					nombre = first.get("value") or first.get("#text") or None
				elif isinstance(lang, dict):
					nombre = lang.get("value") or lang.get("#text") or None
			else:
				if name_field is not None:
					nombre = str(name_field)

			precio = producto.get("price")
			try:
				precio = float(precio) if precio is not None else None
			except Exception:
				precio = None

			activo = producto.get("active")
			try:
				activo = int(activo) if activo is not None else None
			except Exception:
				activo = None

			ref = producto.get("reference")
			if ref is None:
				ref = producto.get("sku") or producto.get("default_code")

			resultado.append({
				"id": int(pid) if pid is not None else None,
				"name": nombre,
				"sku": ref if ref is not None else None,
				"reference": ref if ref is not None else None,
				"price": precio,
				"active": activo,
			})

		return resultado

	except HTTPException as e:
		raise e

	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


def obtener_producto_por_sku_prestashop(sku: str):
	try:
		productos = obtener_productos_prestashop()
		for p in productos:
			# comprobar tanto `reference` como `sku`
			ref = p.get("reference") or p.get("sku")
			if ref is not None and str(ref) == str(sku):
				return p

		# También permitir buscar por id numérico
		for p in productos:
			pid = p.get("id")
			if pid is not None and str(pid) == str(sku):
				return p

		return None

	except HTTPException as e:
		raise e
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))