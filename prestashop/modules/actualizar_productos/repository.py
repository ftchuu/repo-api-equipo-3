from prestashop.core.prestashop_client import prestashop_put, prestashop_get
from lxml import etree

API_KEY = "19KRNWS2GV1UG9MP1FPJMYSVLKYZYAK6"

class ProductoActualizable:

    @staticmethod
    def get_product_id(reference: str):
        res = prestashop_get("products")
        products = res.get("products", [])

        for product in products:
            if isinstance(product, dict) and product.get("reference") == reference:
                return product.get("id")

        return None


    @staticmethod
    def get_product(product_id: int):
        url = f"products/{product_id}"
        res = prestashop_get(url)

        print("URL FINAL:", url)
        print("RESPUESTA:", res)

        # Caso raro: API devuelve lista directa
        if isinstance(res, list):
            return {"product": res[0]}

        # Caso normal listado
        if isinstance(res, dict) and "products" in res:
            return {"product": res["products"][0]}

        # Caso ideal
        if isinstance(res, dict) and "product" in res:
            return res

        raise Exception(f"Formato inesperado de respuesta: {res}")

    
    @staticmethod
    def clean_product(product: dict):

        forbidden = [
            "manufacturer_name",
            "quantity",
            "id_default_image",
            "position_in_category",
            "cache_default_attribute",
            "id_default_combination",
            "associations",
        ]

        for key in forbidden:
            product.pop(key, None)

        return product


    @staticmethod
    def update_product_data(data, price=None, name=None):

        if not isinstance(data, dict) or "product" not in data:
            raise ValueError(f"No se encontró 'product' en respuesta: {data}")

        product = data["product"]

        if not isinstance(product, dict):
            raise ValueError("El campo 'product' no es un dict válido")

        # actualizar precio
        if price is not None:
            product["price"] = str(price)

        # actualizar nombre
        if name is not None:
            names = product.get("name")

            if isinstance(names, list) and len(names) > 0:
                names[0]["value"] = name
            else:
                product["name"] = [{"id": 1, "value": name}]

        product = ProductoActualizable.clean_product(product)
        return {"product": product}


    @staticmethod
    def update_product(product_id: int, xml_data):
        url = f"/products/{product_id}"
        res = prestashop_put(url, xml_data)
        return res
      