from prestashop.core.prestashop_client import prestashop_put, prestashop_get
from lxml import etree

API_KEY = "19KRNWS2GV1UG9MP1FPJMYSVLKYZYAK6"

class ProductoActualizable:

  @staticmethod
  def get_product_id(reference: str):
      res = prestashop_get("products")
      products = res.get("products", [])
  
      for product in products:
          if product.get("reference") == reference:
              return product.get("id")

      return None
  
  @staticmethod
  def get_product_xml(product_id: int):
      url = f"/products/{product_id}"
      res = prestashop_get(url)
      print("URL FINAL:", url)
      return res
  
  @staticmethod
  def update_product_data(data, price=None, name=None):

      product = data["product"]

      if price is not None:
          product["price"] = str(price)

      if name is not None:
          product["name"]["language"][0]["value"] = name

      return {"product": product}
  
  @staticmethod
  def update_product(product_id: int, xml_data):
      url = f"/products/{product_id}"
      res = prestashop_put(url, xml_data)
      res.raise_for_status()
      return res.text
      