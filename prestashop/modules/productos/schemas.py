from pydantic import BaseModel


class Producto(BaseModel):
	id: int | None
	name: str | None
	price: float | None
	active: int | None
	sku: str | None = None
	reference: str | None = None


class ProductoLista(BaseModel):
	total: int
	data: list[Producto]

