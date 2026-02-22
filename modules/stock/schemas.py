from pydantic import BaseModel

class ProductoStock(BaseModel):
    id: int
    name: str
    default_code: str | None = None
    qty_available: float

class StockResponse(BaseModel):
    total: int
    data: list[ProductoStock]