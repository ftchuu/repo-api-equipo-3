from .repository import obtener_clientes

def listar_clientes():
  clientes = obtener_clientes()
  
  return {"total": len(clientes), "data": clientes}