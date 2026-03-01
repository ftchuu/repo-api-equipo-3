from pydantic import BaseModel


class Producto(BaseModel):
    id: int | None = None
    name: str | None = None
    price: float | None = None
    active: int | None = None
    sku: str | None = None
    reference: str | None = None


class ProductoReferencia(BaseModel):
    reference: str


class ProductosMasivos(BaseModel):
    total: int
    data: list[Producto]  # lista de productos creados/actualizados durante la operación
