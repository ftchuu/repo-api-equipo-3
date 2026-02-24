from pydantic import BaseModel

class Pago(BaseModel):
    id: int
    id_order: int
    amount: float
    payment_method: str | None
    date_add: str | None


class PagoLista(BaseModel):
    total: int
    data: list[Pago]