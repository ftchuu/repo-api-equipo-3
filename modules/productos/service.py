import xmlrpc.client
from config import *

def get_products():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

    products = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.product',
        'search_read',
        [[]],
        {
            'fields': ['id', 'name', 'list_price']
        }
    )

    return products