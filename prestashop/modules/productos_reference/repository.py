from fastapi import HTTPException

from prestashop.core.prestashop_client import prestashop_get, prestashop_post, prestashop_put
from prestashop.modules.productos.repository import obtener_producto_por_sku_prestashop


def producto_existe_en_prestashop(reference: str) -> bool:
    # Comprueba si ya hay un producto en PrestaShop con la referencia/sku dada.
    try:
        prod = obtener_producto_por_sku_prestashop(reference)
        return prod is not None
    except HTTPException:
        # por si falla el internet (me resultó útil esta excepción)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def crear_producto_prestashop(data: dict):
    try:
        payload = {"product": data}
        return prestashop_post("products", payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def actualizar_producto_prestashop(product_id: int, data: dict):
    # Actualiza un producto ya existente en PrestaShop (PUT).
    try:
        payload = {"product": data}
        # endpoint: products/{id}
        return prestashop_put(f"products/{product_id}", payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def obtener_stock_available_por_producto(product_id: int) -> dict | None:
    # Obtiene el registro de stock_available asociado a un producto.
    try:
        # forma más confiable: consultar directamente el recurso stock_availables
        data = prestashop_get(f"stock_availables&filter[id_product]=[{product_id}]")
        rows = data.get("stock_availables", [])
        if isinstance(rows, list) and len(rows) > 0 and isinstance(rows[0], dict):
            return rows[0]
        if isinstance(rows, dict):
            return rows
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def actualizar_stock_producto_prestashop(product_id: int, quantity: int):
    # Actualiza la cantidad del producto en stock_availables.
    try:
        stock_row = obtener_stock_available_por_producto(product_id)
        if not stock_row:
            raise HTTPException(
                status_code=500,
                detail="No se encontró stock_available para el producto creado/actualizado",
            )

        stock_id = stock_row.get("id")
        if stock_id is None:
            raise HTTPException(
                status_code=500,
                detail="stock_available encontrado sin id",
            )

        id_shop = stock_row.get("id_shop", 0)
        id_shop_group = stock_row.get("id_shop_group", 0)

        payload = {
            "stock_available": {
                "id": stock_id,
                "id_product": product_id,
                "id_product_attribute": 0,
                "id_shop": id_shop,
                "id_shop_group": id_shop_group,
                "quantity": int(quantity),
                "depends_on_stock": 0,
                "out_of_stock": 2,
            }
        }
        return prestashop_put(f"stock_availables/{stock_id}", payload)
    except HTTPException:
        # error típico cuando la clave no tiene permiso sobre stock_availables
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def validar_permisos_stock_error(error: HTTPException) -> HTTPException:
    # Normaliza errores de permisos de stock_availables para mensajes claros.
    detail = str(error.detail or "")
    if "stock_availables" in detail and ("not allowed" in detail or "401" in detail or "403" in detail):
        return HTTPException(
            status_code=500,
            detail=(
                "La clave Webservice no tiene permisos para 'stock_availables'. "
                "Habilita GET/PUT en ese recurso para sincronizar stock."
            ),
        )
    return error
