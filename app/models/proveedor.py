from typing import Optional
from pydantic import BaseModel, Field


class ProveedorBase(BaseModel):
    cuit: str = Field(..., min_length=1, max_length=20, description="CUIT del proveedor (único)")
    razon_social: str = Field(..., min_length=1, max_length=100, description="Razón Social o Nombre")
    telefono: Optional[str] = Field(None, max_length=30, description="Teléfono de contacto")
    email: Optional[str] = Field(None, max_length=100, description="Correo electrónico")


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(ProveedorBase):
    pass


class ProveedorResponse(ProveedorBase):
    id_proveedor: int

    class Config:
        from_attributes = True
