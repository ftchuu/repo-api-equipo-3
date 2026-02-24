from pydantic import BaseModel

class Proveedor(BaseModel):
    id: int
    name: str | None

class ProveedorLista(BaseModel):
    total: int
    data: list[Proveedor]