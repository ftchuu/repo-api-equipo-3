from pydantic import BaseModel
from datetime import datetime

class Orden(BaseModel):
    id: int
    id_customer: int | None
    total_paid: float | None
    current_state: str | None
    date_add: datetime | None

class OrdenLista(BaseModel):
    total: int
    data: list[Orden]
