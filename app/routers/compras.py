import math
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.templating import templates
from app.database import DatabaseError, RecordNotFoundError
from app.models.compra import CompraCreate
from app.repositories.compra_repo import CompraRepository
from app.repositories.proveedor_repo import ProveedorRepository
from app.repositories.variante_repo import VarianteRepository
from app.services.compra_service import CompraService

router = APIRouter(tags=["Gestión de Compras"])
PAGE_SIZE = 15


# ============================================================================
# VISTAS HTML
# ============================================================================

@router.get("/compras", include_in_schema=False)
def compras_index():
    """Redirecciona al historial de compras."""
    return RedirectResponse(url="/compras/historial")


@router.get("/compras/nueva", response_class=HTMLResponse)
def nueva_compra_form(request: Request):
    """Formulario interactivo para registrar una nueva orden de compra."""
    proveedores = ProveedorRepository.get_all()
    variantes_disponibles = VarianteRepository.get_all_variantes()

    return templates.TemplateResponse(
        "compras/nueva.html",
        {
            "request": request,
            "proveedores": proveedores,
            "variantes_disponibles": variantes_disponibles,
            "active_menu": "compras",
        }
    )


@router.get("/compras/historial", response_class=HTMLResponse)
def list_compras_historial(
    request: Request,
    page: int = Query(1, ge=1),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    id_proveedor: Optional[int] = None
):
    """Historial de compras con filtros de fecha y proveedor."""
    offset = (page - 1) * PAGE_SIZE

    total = CompraRepository.count(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        id_proveedor=id_proveedor
    )

    compras = CompraRepository.get_all(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        id_proveedor=id_proveedor,
        limit=PAGE_SIZE,
        offset=offset
    )

    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1
    proveedores = ProveedorRepository.get_all()

    return templates.TemplateResponse(
        "compras/historial.html",
        {
            "request": request,
            "compras": compras,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "selected_proveedor": id_proveedor,
            "proveedores": proveedores,
            "active_menu": "compras",
        }
    )


@router.get("/compras/{id_compra}", response_class=HTMLResponse)
def ver_detalle_compra(request: Request, id_compra: int):
    """Vista detallada de una orden de compra y sus ítems."""
    try:
        data = CompraService.obtener_compra_completa(id_compra)
    except RecordNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de compra no encontrada.")

    return templates.TemplateResponse(
        "compras/detalle.html",
        {
            "request": request,
            "compra": data["compra"],
            "detalles": data["detalles"],
            "total_unidades": data["total_unidades"],
            "active_menu": "compras",
        }
    )


# ============================================================================
# ENDPOINTS REST (JSON)
# ============================================================================

@router.post("/compras")
def registrar_compra(datos: CompraCreate):
    """Asienta una orden de compra y SUMA stock a las variantes en una transacción atómica."""
    try:
        id_compra = CompraService.registrar_compra(datos)
        return {
            "id_compra": id_compra,
            "message": f"Orden de compra #{id_compra} registrada exitosamente."
        }
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
