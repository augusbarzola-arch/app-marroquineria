from decimal import Decimal
from pydantic import BaseModel, Field


class MedioPagoBase(BaseModel):
    nombre_medio: str = Field(..., min_length=1, max_length=50, description="Nombre del medio de pago")
    porcentaje_descuento_recargo: Decimal = Field(
        default=Decimal("0.00"),
        ge=Decimal("-100.00"),
        le=Decimal("100.00"),
        description="Porcentaje de descuento (negativo) o recargo (positivo). Entre -100 y 100."
    )


class MedioPagoCreate(MedioPagoBase):
    pass


class MedioPagoUpdate(MedioPagoBase):
    pass


class MedioPagoResponse(MedioPagoBase):
    id_medio_pago: int

    class Config:
        from_attributes = True
