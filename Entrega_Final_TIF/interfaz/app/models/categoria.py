from typing import Optional
from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nombre_categoria: str = Field(..., min_length=1, max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción opcional")


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaResponse(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True
