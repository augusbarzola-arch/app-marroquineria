from typing import Optional
from pydantic import BaseModel, Field


class VarianteBase(BaseModel):
    id_color: int = Field(..., gt=0, description="ID del color")
    id_tamano: int = Field(..., gt=0, description="ID del tamaño (sin ñ)")
    stock_actual: int = Field(default=0, ge=0, description="Stock físico actual (>= 0)")
    stock_minimo: int = Field(default=0, ge=0, description="Punto de reposición o stock mínimo (>= 0)")


class VarianteCreate(VarianteBase):
    id_producto: int = Field(..., gt=0, description="ID del producto padre")


class VarianteUpdate(BaseModel):
    id_color: Optional[int] = Field(None, gt=0)
    id_tamano: Optional[int] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)


class VarianteStockQuickUpdate(BaseModel):
    stock_actual: int = Field(..., ge=0)
    stock_minimo: int = Field(..., ge=0)


class VarianteResponse(VarianteBase):
    id_variante: int
    id_producto: int
    nombre_producto: Optional[str] = None
    nombre_color: Optional[str] = None
    nombre_tamano: Optional[str] = None
    precio_costo: Optional[float] = None
    precio_lista: Optional[float] = None

    class Config:
        from_attributes = True
