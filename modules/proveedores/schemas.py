from pydantic import BaseModel

class Proveedor(BaseModel):
    id: int
    name: str
    vat: str | None = None
    email: str | None = None
    phone: str | None = None
    mobile: str | None = None

class ProveedoresResponse(BaseModel):
    total: int
    data: list[Proveedor]