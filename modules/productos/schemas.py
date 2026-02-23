from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    name: str
    default_code: str | None = None
    list_price: float | None = None
    type: str | None = None
    categ_id: list | None = None

class ProductosResponse(BaseModel):
    total: int
    data: list[Producto]
