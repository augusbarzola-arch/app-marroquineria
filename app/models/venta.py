from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ItemVentaCreate(BaseModel):
    id_variante: int = Field(..., gt=0, description="ID de la variante vendida")
    cantidad: int = Field(..., gt=0, description="Cantidad a vender (debe ser mayor a 0)")


class VentaCreate(BaseModel):
    id_medio_pago: int = Field(..., gt=0, description="ID del medio de pago utilizado")
    items: List[ItemVentaCreate] = Field(..., min_length=1, description="Lista de ítems de la venta")


class DetalleVentaResponse(BaseModel):
    renglon_venta: int
    id_variante: int
    nombre_producto: str
    nombre_color: str
    nombre_tamano: str
    cantidad: int
    precio_unitario_cobrado: Decimal
    subtotal: Decimal


class VentaResponse(BaseModel):
    id_venta: int
    fecha_hora: datetime
    monto_total: Decimal
    id_medio_pago: int
    nombre_medio: Optional[str] = None
    porcentaje_descuento_recargo: Optional[Decimal] = None
    detalles: Optional[List[DetalleVentaResponse]] = None

    class Config:
        from_attributes = True
