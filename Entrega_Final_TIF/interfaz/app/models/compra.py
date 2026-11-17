from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ItemCompraCreate(BaseModel):
    id_variante: int = Field(..., gt=0, description="ID de la variante comprada")
    cantidad: int = Field(..., gt=0, description="Cantidad comprada (debe ser mayor a 0)")
    precio_costo_unitario: Decimal = Field(..., ge=Decimal("0.00"), description="Precio de costo unitario pactado (>= 0)")


class CompraCreate(BaseModel):
    id_proveedor: int = Field(..., gt=0, description="ID del proveedor de la orden de compra")
    items: List[ItemCompraCreate] = Field(..., min_length=1, description="Lista de ítems comprados")


class DetalleCompraResponse(BaseModel):
    renglon_compra: int
    id_variante: int
    nombre_producto: str
    nombre_color: str
    nombre_tamano: str
    cantidad: int
    precio_costo_unitario: Decimal
    subtotal: Decimal


class CompraResponse(BaseModel):
    id_compra: int
    fecha_compra: datetime
    monto_total: Decimal
    id_proveedor: int
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    detalles: Optional[List[DetalleCompraResponse]] = None

    class Config:
        from_attributes = True
