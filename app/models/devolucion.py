from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field


MotivoDevolucion = Literal["CAMBIO", "REPARACION", "DEVOLUCION"]


class DevolucionCreate(BaseModel):
    id_venta: int = Field(..., gt=0, description="ID de la venta original")
    id_variante_devuelta: int = Field(..., gt=0, description="ID de la variante que devuelve el cliente")
    cantidad: int = Field(..., gt=0, description="Cantidad devuelta (no puede superar la cantidad vendida)")
    motivo: MotivoDevolucion = Field(..., description="Motivo: CAMBIO, REPARACION o DEVOLUCION")
    id_variante_nueva: Optional[int] = Field(None, gt=0, description="ID de la variante nueva entregada (obligatorio en CAMBIO)")
    monto_diferencia: Optional[Decimal] = Field(Decimal("0.00"), description="Diferencia de precio calculada")
    observaciones: Optional[str] = Field(None, max_length=255, description="Observaciones opcionales")


class DevolucionResponse(BaseModel):
    id_devolucion: int
    fecha: datetime
    id_venta: int
    id_variante_devuelta: int
    cantidad: int
    motivo: MotivoDevolucion
    id_variante_nueva: Optional[int] = None
    monto_diferencia: Decimal
    observaciones: Optional[str] = None
    nombre_producto_devuelto: Optional[str] = None
    nombre_producto_nuevo: Optional[str] = None

    class Config:
        from_attributes = True
