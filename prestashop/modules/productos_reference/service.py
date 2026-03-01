from core.odoo import get_odoo_connection, ODOO_DB, ODOO_PASSWORD
from fastapi import HTTPException
import re
import unicodedata

from .repository import (
    producto_existe_en_prestashop,
    crear_producto_prestashop,
    actualizar_producto_prestashop,
    actualizar_stock_producto_prestashop,
    validar_permisos_stock_error,
)


def _slugify(value: str) -> str:
    text = str(value or "producto").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text or "producto"


def _multilang(value: str) -> dict:
    text = str(value or "")
    # compatibilidad para instalaciones con id de idioma 1 y 2
    return {"language": [{"id": 1, "value": text}, {"id": 2, "value": text}]}


def buscar_producto_por_referencia(reference: str) -> dict:
    """Retorna el producto de Odoo que tenga `default_code` igual a la
    referencia proporcionada.

    Lanza HTTPException(404) si no existe. Devuelve un diccionario con los
    campos normalizados acorde al esquema `Producto` usado en las respuestas
    de PrestaShop.
    """
    uid, models = get_odoo_connection()

    productos = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "product.product",
        "search_read",
        [[("default_code", "=", reference)]],
        {"fields": ["id", "name", "default_code", "list_price", "type", "qty_available"]},
    )

    if not productos:
        raise HTTPException(status_code=404, detail="Producto no encontrado en Odoo")

    # cuando hay referencias duplicadas en Odoo, priorizar el de mayor stock;
    # en empate usar el id más alto (registro más reciente).
    productos_ordenados = sorted(
        productos,
        key=lambda x: (float(x.get("qty_available") or 0), int(x.get("id") or 0)),
        reverse=True,
    )
    prod = productos_ordenados[0]
    # normalizar y dejar algunos campos auxiliares para uso interno
    price_val = float(prod.get("list_price")) if prod.get("list_price") is not None else 0
    stock_val = prod.get("qty_available") or 0
    return {
        "id": prod.get("id"),
        "name": prod.get("name"),
        "price": price_val,
        "active": None,
        "sku": prod.get("default_code"),
        "reference": prod.get("default_code"),
        # campos extras para la lógica de creación
        "_odoo_price": price_val,
        "_odoo_stock": stock_val,
    }


def crear_producto_por_referencia(reference: str):
    """Busca un producto en Odoo y lo crea en PrestaShop.

    Se apoyan las mismas reglas de negocio que antes pero la obtención
    del producto se delega a `buscar_producto_por_referencia` para evitar
    duplicación de código.
    """
    try:
        prod = buscar_producto_por_referencia(reference)
        product_name = prod.get("name") or "Producto"
        product_slug = _slugify(product_name)

        # los valores que necesitamos ya vienen normalizados en el diccionario
        price = prod.get("_odoo_price") or 0
        stock = prod.get("_odoo_stock") or 0

        # validaciones de precio/stock
        if price == 0 and stock == 0:
            raise HTTPException(
                status_code=400,
                detail="No se pueden crear productos con precio 0 y stock 0",
            )

        # si ya existe en PrestaShop, intentar actualizarlo si le faltan
        # campos relevantes (categoría o activo). De lo contrario devolver
        # el producto existente para hacer la operación idempotente.
        if producto_existe_en_prestashop(reference):
            from prestashop.modules.productos.repository import obtener_producto_por_sku_prestashop

            existente = obtener_producto_por_sku_prestashop(reference)
            if existente is None:
                # no debería ocurrir pero lo manejamos
                raise HTTPException(status_code=500, detail="Error al comprobar producto existente en PrestaShop")

            # comprobar si necesita actualización: categoría vacía o no activo
            needs_update = False
            try:
                cid = existente.get("id_category_default")
                if cid in (None, 0, "0"):
                    needs_update = True
            except Exception:
                needs_update = True

            try:
                active_val = existente.get("active")
                if active_val in (None, 0, "0", "false", False):  
                    needs_update = True
            except Exception:
                needs_update = True

            if needs_update:
                prod_id = existente.get("id")
                update_data = {
                    "id": prod_id,
                    "name": _multilang(product_name),
                    "link_rewrite": _multilang(product_slug),
                    "price": float(price),
                    "reference": prod.get("reference") or prod.get("sku"),
                    "id_tax_rules_group": 1,
                    "id_category_default": 1,
                    "active": 1,
                    "state": 1,
                    "product_type": "standard",
                    "visibility": "both",
                    "available_for_order": 1,
                    "show_price": 1,
                    "associations": {"categories": {"category": [{"id": "1"}]}}
                }
                actualizar_producto_prestashop(prod_id, update_data)
                try:
                    actualizar_stock_producto_prestashop(int(prod_id), int(stock))
                except HTTPException as e:
                    raise validar_permisos_stock_error(e)
                from prestashop.modules.productos.repository import obtener_producto_por_sku_prestashop
                return obtener_producto_por_sku_prestashop(reference)

            # aunque no necesite actualizar campos de producto, sí sincronizamos stock
            existente_id = existente.get("id")
            if existente_id is not None:
                try:
                    actualizar_stock_producto_prestashop(int(existente_id), int(stock))
                except HTTPException as e:
                    raise validar_permisos_stock_error(e)

            # si no necesita update devolvemos el producto existente
            return existente

        # construir payload para PrestaShop
        ps_data = {
            "name": _multilang(product_name),
            "link_rewrite": _multilang(product_slug),
            "price": float(price),
            # la referencia está en los campos normalizados SKU / reference
            "reference": prod.get("reference") or prod.get("sku"),
            "active": 1,
            "state": 1,
            "product_type": "standard",
            "id_tax_rules_group": 1,
            "visibility": "both",
            "available_for_order": 1,
            "show_price": 1,
            # configuración de categorías necesaria para visibilidad
            "id_category_default": 1,
            "associations": {
                "categories": {"category": [{"id": "1"}]}
            },
        }

        created = crear_producto_prestashop(ps_data)

        pid = None
        if isinstance(created, dict):
            # la respuesta de POST suele devolver { 'product': { 'id': 'X', ... }}
            prod_node = created.get("product") or {}
            pid = prod_node.get("id")

        if pid:
            from prestashop.core.prestashop_client import prestashop_get
            data_products = prestashop_get("products")
            productos = data_products.get("products", [])

            product_row = None
            for item in productos:
                try:
                    if int(item.get("id")) == int(pid):
                        product_row = item
                        break
                except Exception:
                    continue

            category_default = None
            if isinstance(product_row, dict):
                category_default = product_row.get("id_category_default")

            # si no hay categoría default válida, avisamos al cliente
            if category_default in (None, 0, "0", ""):
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "El producto se creó pero no tiene categoría asignada. "
                        "Revisa los permisos de la clave de PrestaShop."
                    ),
                )

            # sincronizar stock de Odoo hacia PrestaShop
            try:
                actualizar_stock_producto_prestashop(int(pid), int(stock))
            except HTTPException as e:
                raise validar_permisos_stock_error(e)

        from prestashop.modules.productos.repository import obtener_producto_por_sku_prestashop
        return obtener_producto_por_sku_prestashop(reference)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def crear_productos_masivamente():
   
    uid, models = get_odoo_connection()
    try:
        productos_odoo = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASSWORD,
            "product.product",
            "search_read",
            [[]],  # se pueden añadir filtros si se desea limitar la consulta
            {"fields": ["id", "name", "default_code", "list_price", "qty_available"]},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando Odoo: {e}")

    resultados = []

    for prod in productos_odoo:
        reference = prod.get("default_code")
        price = float(prod.get("list_price") or 0)
        stock = prod.get("qty_available") or 0

        # reglas de exclusión
        if not reference:
            continue
        if price == 0 and stock == 0:
            continue

        try:
            # la función ya maneja existencia/actualización y validaciones
            creado = crear_producto_por_referencia(reference)
            resultados.append(creado)
        except HTTPException as httpe:
            # si hay un error específico de un producto podemos continuar
            # (podría guardarse en un log o en una lista de errores)
            continue
        except Exception:
            # ignorar cualquier otra excepción individual
            continue

    return {"total": len(resultados), "data": resultados}
