import requests
from fastapi import HTTPException

BASE_URL = "http://localhost:8080/api"
API_KEY = "5CBDJD9A6EVGMWVM4SVPPQW6VD3LGHMR"  # Reemplaza con tu API Key de PrestaShop


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