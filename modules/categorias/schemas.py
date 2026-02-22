from pydantic import BaseModel

class Categoria(BaseModel):
    id: int
    name: str
    complete_name: str


class CategoriaResponse(BaseModel):
    total: int
    data: list[Categoria]