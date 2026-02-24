from pydantic import BaseModel


class OrdenReferencia(BaseModel):
    id: int | None
    reference: str | None
    total_paid: float | None
    date_add: str | None
    current_state: str | None


class OrdenReferenciaLista(BaseModel):
    total: int
    data: list[OrdenReferencia]
