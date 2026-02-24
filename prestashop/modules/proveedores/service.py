from .repository import obtener_proveedores

def listar_proveedores():
    proveedores = obtener_proveedores()
    
    return {"total": len(proveedores), "data": proveedores}