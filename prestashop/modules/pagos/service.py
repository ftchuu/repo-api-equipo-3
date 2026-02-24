from .repository import obtener_pagos

def listar_pagos():
  pagos = obtener_pagos()
  
  return {"total": len(pagos), "data": pagos}