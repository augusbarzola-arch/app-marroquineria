from pydantic import BaseModel, Field


class MaterialBase(BaseModel):
    nombre_material: str = Field(..., min_length=1, max_length=50, description="Nombre del material")


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    id_material: int

    class Config:
        from_attributes = True
