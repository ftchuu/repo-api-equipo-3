import requests
from fastapi import HTTPException

BASE_URL = "https://mitienda.com/api"
API_KEY = "TU_API_KEY"


def prestashop_get(endpoint: str):
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, auth=(API_KEY, ""))
        response.raise_for_status()
        return response.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))