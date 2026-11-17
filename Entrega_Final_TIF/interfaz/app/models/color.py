from pydantic import BaseModel, Field


class ColorBase(BaseModel):
    nombre_color: str = Field(..., min_length=1, max_length=30, description="Nombre del color (único)")


class ColorCreate(ColorBase):
    pass


class ColorUpdate(ColorBase):
    pass


class ColorResponse(ColorBase):
    id_color: int

    class Config:
        from_attributes = True
