from pydantic import BaseModel
from typing import Optional

class ProductoActualizar(BaseModel):
    reference: str
    name: Optional[str] = None
    price: Optional[float] = None