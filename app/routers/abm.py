import math
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

from app.templating import templates
from app.database import (
    DatabaseError,
    RecordNotFoundError,
    UniqueConstraintError,
    ForeignKeyConstraintError,
)
from app.models.categoria import CategoriaCreate, CategoriaUpdate
from app.models.material import MaterialCreate, MaterialUpdate
from app.models.color import ColorCreate, ColorUpdate
from app.models.tamano import TamanoCreate, TamanoUpdate
from app.models.proveedor import ProveedorCreate, ProveedorUpdate
from app.models.medio_pago import MedioPagoCreate, MedioPagoUpdate

from app.repositories.categoria_repo import CategoriaRepository
from app.repositories.material_repo import MaterialRepository
from app.repositories.color_repo import ColorRepository
from app.repositories.tamano_repo import TamanoRepository
from app.repositories.proveedor_repo import ProveedorRepository
from app.repositories.medio_pago_repo import MedioPagoRepository

router = APIRouter(tags=["ABM Entidades Simples"])
PAGE_SIZE = 10


# ============================================================================
# 1. CATEGORÍAS
# ============================================================================

@router.get("/categorias", response_class=HTMLResponse)
def list_categorias(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = CategoriaRepository.count(search=search)
    items = CategoriaRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/categorias.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "categorias",
        }
    )

@router.post("/categorias")
def create_categoria(data: CategoriaCreate):
    try:
        new_id = CategoriaRepository.create(
            nombre_categoria=data.nombre_categoria,
            descripcion=data.descripcion
        )
        return {"id_categoria": new_id, "message": "Categoría creada exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/categorias/{id_categoria}")
def update_categoria(id_categoria: int, data: CategoriaUpdate):
    try:
        CategoriaRepository.update(
            id_categoria=id_categoria,
            nombre_categoria=data.nombre_categoria,
            descripcion=data.descripcion
        )
        return {"message": "Categoría actualizada exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/categorias/{id_categoria}")
def delete_categoria(id_categoria: int):
    try:
        CategoriaRepository.delete(id_categoria)
        return {"message": "Categoría eliminada con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# 2. MATERIALES
# ============================================================================

@router.get("/materiales", response_class=HTMLResponse)
def list_materiales(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = MaterialRepository.count(search=search)
    items = MaterialRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/materiales.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "materiales",
        }
    )

@router.post("/materiales")
def create_material(data: MaterialCreate):
    try:
        new_id = MaterialRepository.create(nombre_material=data.nombre_material)
        return {"id_material": new_id, "message": "Material creado exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/materiales/{id_material}")
def update_material(id_material: int, data: MaterialUpdate):
    try:
        MaterialRepository.update(id_material=id_material, nombre_material=data.nombre_material)
        return {"message": "Material actualizado exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/materiales/{id_material}")
def delete_material(id_material: int):
    try:
        MaterialRepository.delete(id_material)
        return {"message": "Material eliminado con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# 3. COLORES
# ============================================================================

@router.get("/colores", response_class=HTMLResponse)
def list_colores(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = ColorRepository.count(search=search)
    items = ColorRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/colores.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "colores",
        }
    )

@router.post("/colores")
def create_color(data: ColorCreate):
    try:
        new_id = ColorRepository.create(nombre_color=data.nombre_color)
        return {"id_color": new_id, "message": "Color creado exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/colores/{id_color}")
def update_color(id_color: int, data: ColorUpdate):
    try:
        ColorRepository.update(id_color=id_color, nombre_color=data.nombre_color)
        return {"message": "Color actualizado exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/colores/{id_color}")
def delete_color(id_color: int):
    try:
        ColorRepository.delete(id_color)
        return {"message": "Color eliminado con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# 4. TAMAÑOS (TAMANO)
# ============================================================================

@router.get("/tamanos", response_class=HTMLResponse)
def list_tamanos(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = TamanoRepository.count(search=search)
    items = TamanoRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/tamanos.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "tamanos",
        }
    )

@router.post("/tamanos")
def create_tamano(data: TamanoCreate):
    try:
        new_id = TamanoRepository.create(nombre_tamano=data.nombre_tamano)
        return {"id_tamano": new_id, "message": "Tamaño creado exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/tamanos/{id_tamano}")
def update_tamano(id_tamano: int, data: TamanoUpdate):
    try:
        TamanoRepository.update(id_tamano=id_tamano, nombre_tamano=data.nombre_tamano)
        return {"message": "Tamaño actualizado exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/tamanos/{id_tamano}")
def delete_tamano(id_tamano: int):
    try:
        TamanoRepository.delete(id_tamano)
        return {"message": "Tamaño eliminado con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# 5. PROVEEDORES
# ============================================================================

@router.get("/proveedores", response_class=HTMLResponse)
def list_proveedores(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = ProveedorRepository.count(search=search)
    items = ProveedorRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/proveedores.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "proveedores",
        }
    )

@router.post("/proveedores")
def create_proveedor(data: ProveedorCreate):
    try:
        new_id = ProveedorRepository.create(
            cuit=data.cuit,
            razon_social=data.razon_social,
            telefono=data.telefono,
            email=data.email
        )
        return {"id_proveedor": new_id, "message": "Proveedor creado exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/proveedores/{id_proveedor}")
def update_proveedor(id_proveedor: int, data: ProveedorUpdate):
    try:
        ProveedorRepository.update(
            id_proveedor=id_proveedor,
            cuit=data.cuit,
            razon_social=data.razon_social,
            telefono=data.telefono,
            email=data.email
        )
        return {"message": "Proveedor actualizado exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/proveedores/{id_proveedor}")
def delete_proveedor(id_proveedor: int):
    try:
        ProveedorRepository.delete(id_proveedor)
        return {"message": "Proveedor eliminado con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# 6. MEDIOS DE PAGO
# ============================================================================

@router.get("/medios-pago", response_class=HTMLResponse)
def list_medios_pago(
    request: Request,
    page: int = Query(1, ge=1),
    search: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE
    total = MedioPagoRepository.count(search=search)
    items = MedioPagoRepository.get_all(search=search, limit=PAGE_SIZE, offset=offset)
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "abm/medios_pago.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "active_menu": "medios_pago",
        }
    )

@router.post("/medios-pago")
def create_medio_pago(data: MedioPagoCreate):
    try:
        new_id = MedioPagoRepository.create(
            nombre_medio=data.nombre_medio,
            porcentaje_descuento_recargo=data.porcentaje_descuento_recargo
        )
        return {"id_medio_pago": new_id, "message": "Medio de pago creado exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/medios-pago/{id_medio_pago}")
def update_medio_pago(id_medio_pago: int, data: MedioPagoUpdate):
    try:
        MedioPagoRepository.update(
            id_medio_pago=id_medio_pago,
            nombre_medio=data.nombre_medio,
            porcentaje_descuento_recargo=data.porcentaje_descuento_recargo
        )
        return {"message": "Medio de pago actualizado exitosamente."}
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/medios-pago/{id_medio_pago}")
def delete_medio_pago(id_medio_pago: int):
    try:
        MedioPagoRepository.delete(id_medio_pago)
        return {"message": "Medio de pago eliminado con éxito."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# ENDPOINTS API AUXILIARES (para selects y dropdowns futuros)
# ============================================================================

@router.get("/api/categorias")
def api_categorias():
    return CategoriaRepository.get_all()

@router.get("/api/materiales")
def api_materiales():
    return MaterialRepository.get_all()

@router.get("/api/colores")
def api_colores():
    return ColorRepository.get_all()

@router.get("/api/tamanos")
def api_tamanos():
    return TamanoRepository.get_all()

@router.get("/api/proveedores")
def api_proveedores():
    return ProveedorRepository.get_all()

@router.get("/api/medios-pago")
def api_medios_pago():
    return MedioPagoRepository.get_all()
