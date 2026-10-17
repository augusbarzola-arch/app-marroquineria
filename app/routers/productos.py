import math
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

from app.templating import templates
from app.query_params import OptionalIntQuery, OptionalStrQuery
from app.database import (
    DatabaseError,
    RecordNotFoundError,
    UniqueConstraintError,
    ForeignKeyConstraintError,
)
from app.models.producto import ProductoCreate, ProductoUpdate
from app.models.variante import VarianteCreate, VarianteUpdate
from app.repositories.producto_repo import ProductoRepository
from app.repositories.variante_repo import VarianteRepository
from app.repositories.categoria_repo import CategoriaRepository
from app.repositories.material_repo import MaterialRepository
from app.repositories.color_repo import ColorRepository
from app.repositories.tamano_repo import TamanoRepository
from app.services.producto_service import ProductoService

router = APIRouter(tags=["Gestión de Productos"])
PAGE_SIZE = 10


# ============================================================================
# VISTAS HTML
# ============================================================================

@router.get("/productos", response_class=HTMLResponse)
def list_productos(
    request: Request,
    page: int = Query(1, ge=1),
    search: OptionalStrQuery = None,
    id_categoria: OptionalIntQuery = None,
    id_material: OptionalIntQuery = None
):
    """Listado paginado de productos con filtros por categoría, material y texto."""
    # Selects "Todos" envían "" y no deben romperse como int inválido.
    offset = (page - 1) * PAGE_SIZE
    total = ProductoRepository.count(
        search=search,
        id_categoria=id_categoria,
        id_material=id_material
    )
    items = ProductoRepository.get_all(
        search=search,
        id_categoria=id_categoria,
        id_material=id_material,
        limit=PAGE_SIZE,
        offset=offset
    )
    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    categorias = CategoriaRepository.get_all()
    materiales = MaterialRepository.get_all()

    return templates.TemplateResponse(
        "productos/listado.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "selected_categoria": id_categoria,
            "selected_material": id_material,
            "categorias": categorias,
            "materiales": materiales,
            "active_menu": "productos",
        }
    )


@router.get("/productos/nuevo", response_class=HTMLResponse)
def nuevo_producto_form(request: Request):
    """Formulario para la creación de un nuevo producto."""
    categorias = CategoriaRepository.get_all()
    materiales = MaterialRepository.get_all()
    return templates.TemplateResponse(
        "productos/form.html",
        {
            "request": request,
            "is_edit": False,
            "producto": None,
            "categorias": categorias,
            "materiales": materiales,
            "active_menu": "productos",
        }
    )


@router.get("/productos/{id_producto}/editar", response_class=HTMLResponse)
def editar_producto_form(request: Request, id_producto: int):
    """Formulario para la edición de un producto existente."""
    producto = ProductoRepository.get_by_id(id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    categorias = CategoriaRepository.get_all()
    materiales = MaterialRepository.get_all()
    return templates.TemplateResponse(
        "productos/form.html",
        {
            "request": request,
            "is_edit": True,
            "producto": producto,
            "categorias": categorias,
            "materiales": materiales,
            "active_menu": "productos",
        }
    )


@router.get("/productos/{id_producto}", response_class=HTMLResponse)
def detalle_producto(request: Request, id_producto: int):
    """Vista detallada del producto con sus variantes y opciones para agregar/editar."""
    try:
        detalle = ProductoService.obtener_detalle(id_producto)
    except RecordNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    colores = ColorRepository.get_all()
    tamanos = TamanoRepository.get_all()

    return templates.TemplateResponse(
        "productos/detalle.html",
        {
            "request": request,
            "producto": detalle["producto"],
            "variantes": detalle["variantes"],
            "margen_porcentaje": detalle["margen_porcentaje"],
            "total_stock": detalle["total_stock"],
            "total_variantes": detalle["total_variantes"],
            "colores": colores,
            "tamanos": tamanos,
            "active_menu": "productos",
        }
    )


# ============================================================================
# ENDPOINTS REST (JSON)
# ============================================================================

@router.post("/productos")
def create_producto(datos: ProductoCreate):
    """Crea un producto nuevo. Emite advertencia si precio_lista < precio_costo."""
    try:
        new_id, advertencia = ProductoService.crear_producto(datos)
        return {
            "id_producto": new_id,
            "advertencia": advertencia,
            "message": "Producto creado exitosamente."
        }
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/productos/{id_producto}")
def update_producto(id_producto: int, datos: ProductoUpdate):
    """Actualiza un producto existente."""
    try:
        _, advertencia = ProductoService.actualizar_producto(id_producto, datos)
        return {
            "message": "Producto actualizado exitosamente.",
            "advertencia": advertencia
        }
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/productos/{id_producto}")
def delete_producto(id_producto: int):
    """Elimina un producto y sus variantes si no tienen operaciones registradas."""
    try:
        ProductoService.eliminar_producto(id_producto)
        return {"message": "Producto y variantes eliminados exitosamente."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# GESTIÓN DE VARIANTES VINCULADAS AL PRODUCTO
# ============================================================================

@router.post("/productos/{id_producto}/variantes")
def create_variante_producto(id_producto: int, datos: VarianteCreate):
    """Agrega una variante al producto especificado."""
    if datos.id_producto != id_producto:
        datos.id_producto = id_producto

    try:
        new_id = ProductoService.crear_variante(datos)
        return {"id_variante": new_id, "message": "Variante agregada exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/productos/{id_producto}/variantes/{id_variante}")
def update_variante_producto(id_producto: int, id_variante: int, datos: VarianteUpdate):
    """Actualiza una variante de un producto."""
    try:
        var = VarianteRepository.get_by_id(id_variante)
        if not var or var["id_producto"] != id_producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variante no encontrada en este producto.")

        ProductoService.actualizar_variante(
            id_variante=id_variante,
            id_color=datos.id_color if datos.id_color is not None else var["id_color"],
            id_tamano=datos.id_tamano if datos.id_tamano is not None else var["id_tamano"],
            stock_actual=datos.stock_actual if datos.stock_actual is not None else var["stock_actual"],
            stock_minimo=datos.stock_minimo if datos.stock_minimo is not None else var["stock_minimo"]
        )
        return {"message": "Variante actualizada exitosamente."}
    except (UniqueConstraintError, DatabaseError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/productos/{id_producto}/variantes/{id_variante}")
def delete_variante_producto(id_producto: int, id_variante: int):
    """Elimina una variante si no tiene ventas, compras o devoluciones."""
    try:
        var = VarianteRepository.get_by_id(id_variante)
        if not var or var["id_producto"] != id_producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variante no encontrada en este producto.")

        ProductoService.eliminar_variante(id_variante)
        return {"message": "Variante eliminada exitosamente."}
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
