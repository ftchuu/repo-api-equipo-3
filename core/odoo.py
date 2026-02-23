import xmlrpc.client
from fastapi import HTTPException

ODOO_URL = "http://localhost:8069"
ODOO_DB = "Modelo-test"
ODOO_USERNAME = "15234853@modelo.edu.mx"
ODOO_PASSWORD = "Richivalens#27"


def get_odoo_connection():
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        if not uid:
            raise Exception("Autenticación fallida")

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        return uid, models

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))