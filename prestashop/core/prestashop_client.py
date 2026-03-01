import os
import requests
from fastapi import HTTPException

base = os.getenv("PRESTASHOP_BASE_URL", "http://localhost:8080/api")
# eliminar barra final para normalizar
base = base.rstrip("/")
if not base.endswith("/api"):
    base = f"{base}/api"
BASE_URL = base

API_KEY = os.getenv("PRESTASHOP_API_KEY", "U658XXUZ9CQC2JFNUDGSN4WGP7C81UQE")
if not API_KEY:
    # no usamos HTTPException aquí porque esto ocurre durante la carga del
    # módulo y queremos que la aplicación falle rápido.
    raise RuntimeError("PRESTASHOP_API_KEY no está configurada. Defina la variable de entorno correspondiente.")


def prestashop_get(endpoint: str):
    url = f"{BASE_URL}/{endpoint}?output_format=JSON&display=full"

    try:
        response = requests.get(url, auth=(API_KEY, ""))

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Autenticación fallida")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar a PrestaShop")
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Tiempo de espera agotado al conectar con PrestaShop")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def prestashop_put(endpoint: str, payload: dict):
    """Helper para enviar datos a PrestaShop mediante PUT (actualizaciones).

    Construye el XML igual que `prestashop_post` pero realiza un PUT al
    recurso indicado (por ejemplo `products/{id}`).
    """
    def _dict_to_xml(tag: str, value):
        if isinstance(value, dict) and set(value.keys()) == {"id", "value"}:
            return f"<{tag} id=\"{value['id']}\">{value['value']}</{tag}>"

        if isinstance(value, dict):
            inner = "".join(_dict_to_xml(k, v) for k, v in value.items())
            return f"<{tag}>{inner}</{tag}>"

        if isinstance(value, list):
            return "".join(_dict_to_xml(tag, item) for item in value)

        return f"<{tag}>{value}</{tag}>"

    xml_body = "<prestashop>"
    for k, v in payload.items():
        xml_body += _dict_to_xml(k, v)
    xml_body += "</prestashop>"

    url = f"{BASE_URL}/{endpoint}?output_format=JSON"
    headers = {"Content-Type": "application/xml"}

    try:
        response = requests.put(url, data=xml_body.encode("utf-8"), headers=headers, auth=(API_KEY, ""))

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Autenticación fallida")

        if response.status_code >= 400:
            text = response.text
            raise HTTPException(status_code=response.status_code, detail=text)

        return response.json()

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar a PrestaShop")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Tiempo de espera agotado al conectar con PrestaShop")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def prestashop_post(endpoint: str, payload: dict):
    
    # conversión sencilla de diccionario a XML válido para PrestaShop
    def _dict_to_xml(tag: str, value):
        # caso base: diccionario con id+value se convierte en etiqueta con
        # atributo `id` y texto contenido
        if isinstance(value, dict) and set(value.keys()) == {"id", "value"}:
            return f"<{tag} id=\"{value['id']}\">{value['value']}</{tag}>"

        if isinstance(value, dict):
            inner = "".join(_dict_to_xml(k, v) for k, v in value.items())
            return f"<{tag}>{inner}</{tag}>"

        if isinstance(value, list):
            return "".join(_dict_to_xml(tag, item) for item in value)

        # primitivo
        return f"<{tag}>{value}</{tag}>"

    xml_body = "<prestashop>"
    for k, v in payload.items():
        xml_body += _dict_to_xml(k, v)
    xml_body += "</prestashop>"

    url = f"{BASE_URL}/{endpoint}?output_format=JSON"
    headers = {"Content-Type": "application/xml"}

    try:
        response = requests.post(url, data=xml_body.encode("utf-8"), headers=headers, auth=(API_KEY, ""))

        # si hay un error de autenticación lo devolvemos de forma clara
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Autenticación fallida")

        if response.status_code >= 400:
            text = response.text
            raise HTTPException(status_code=response.status_code, detail=text)

        return response.json()

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar a PrestaShop")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Tiempo de espera agotado al conectar con PrestaShop")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))