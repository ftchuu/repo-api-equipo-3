from .repository import obtener_ordenes_repository
from .schemas import OrdenLista, Orden

def obtener_ordenes_service():
    ordenes = obtener_ordenes_repository()

    data = []

    for orden in ordenes:
        data.append(
            Orden(
                id=orden.get("id"),
                id_customer=orden.get("id_customer"),
                total_paid=orden.get("total_paid"),
                current_state=orden.get("current_state"),
                date_add=orden.get("date_add"),
            )
        )

    return OrdenLista(
        total=len(data),
        data=data
    )
