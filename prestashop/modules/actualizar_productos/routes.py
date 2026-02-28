from fastapi import APIRouter, HTTPException
from prestashop.modules.actualizar_productos.schemas import ProductoActualizar
from .repository import ProductoActualizable

router = APIRouter()

@router.put("/actualizar_producto")
def actualizar_producto(data: ProductoActualizar):
    try:
        # 1. Obtener el ID del producto a actualizar usando la referencia (SKU)
        product_id = ProductoActualizable.get_product_id(data.reference)
        if not product_id:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # 2. Obtener el XML actual del producto
        xml_data = ProductoActualizable.get_product_xml(product_id)

        # 3. Modificar el XML con los nuevos datos
        updated_xml = ProductoActualizable.update_product_data(
            xml_data,
            price=data.price,
            name=data.name,
        )

        # 4. Enviar el XML actualizado a PrestaShop
        ProductoActualizable.update_product(product_id, updated_xml)

        return {"message": "Producto actualizado exitosamente"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/test")
def test():
    return ProductoActualizable.get_product_id("NHD-0001")
    