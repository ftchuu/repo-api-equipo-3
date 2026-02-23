from pydantic import BaseModel
from typing import List, Optional


class Orden(BaseModel):
    id: int
    name: str
    date_order: str | None = None
    amount_total: float | None = None
    state: str | None = None
    partner_id: list | None = None


class OrdenesResponse(BaseModel):
    total: int
    data: List[Orden]
