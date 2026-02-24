

from .repository import obtener_productos_prestashop, obtener_producto_por_sku_prestashop


def listar_productos():
	try:
		productos = obtener_productos_prestashop()
		return {"total": len(productos), "data": productos}
	except Exception as e:
		raise e


def buscar_producto_por_sku(sku: str):
	try:
		p = obtener_producto_por_sku_prestashop(sku)
		if p is None:
			from fastapi import HTTPException
			raise HTTPException(status_code=404, detail="Producto no encontrado en PrestaShop")
		return p
	except HTTPException:
		raise
	except Exception as e:
		from fastapi import HTTPException
		raise HTTPException(status_code=500, detail=str(e))

