from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    firstname: str | None
    lastname: str | None
    email: str | None

class ClienteLista(BaseModel):
    total: int
    data: list[Cliente]