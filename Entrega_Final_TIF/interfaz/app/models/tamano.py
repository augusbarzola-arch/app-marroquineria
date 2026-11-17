from pydantic import BaseModel, Field


class TamanoBase(BaseModel):
    nombre_tamano: str = Field(..., min_length=1, max_length=20, description="Nombre del tamaño/talle (único, sin ñ)")


class TamanoCreate(TamanoBase):
    pass


class TamanoUpdate(TamanoBase):
    pass


class TamanoResponse(TamanoBase):
    id_tamano: int

    class Config:
        from_attributes = True
