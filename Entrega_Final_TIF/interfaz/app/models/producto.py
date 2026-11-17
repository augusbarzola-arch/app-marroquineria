from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    sku: Optional[str] = Field(None, max_length=30, description="Código SKU único del producto")
    nombre_producto: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción opcional")
    precio_costo: Decimal = Field(..., ge=Decimal("0.00"), description="Precio de costo (>= 0)")
    precio_lista: Decimal = Field(..., ge=Decimal("0.00"), description="Precio de venta de lista (>= 0)")
    id_categoria: int = Field(..., gt=0, description="ID de la categoría")
    id_material: int = Field(..., gt=0, description="ID del material")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoResponse(ProductoBase):
    id_producto: int
    nombre_categoria: Optional[str] = None
    nombre_material: Optional[str] = None
    total_variantes: Optional[int] = 0
    stock_total: Optional[int] = 0

    class Config:
        from_attributes = True
