import math
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.templating import templates
from app.database import DatabaseError, RecordNotFoundError
from app.models.devolucion import DevolucionCreate
from app.repositories.devolucion_repo import DevolucionRepository
from app.repositories.venta_repo import VentaRepository
from app.repositories.variante_repo import VarianteRepository
from app.services.devolucion_service import DevolucionService

router = APIRouter(tags=["Gestión de Devoluciones"])
PAGE_SIZE = 15


# ============================================================================
# VISTAS HTML
# ============================================================================

@router.get("/devoluciones", include_in_schema=False)
def devoluciones_index():
    """Redirecciona al historial de devoluciones."""
    return RedirectResponse(url="/devoluciones/historial")


@router.get("/devoluciones/nueva", response_class=HTMLResponse)
def nueva_devolucion_form(
    request: Request,
    id_venta: Optional[int] = None
):
    """Formulario guiado para registrar Devolución, Cambio o Reparación."""
    variantes_disponibles = VarianteRepository.get_all_variantes()

    return templates.TemplateResponse(
        "devoluciones/nueva.html",
        {
            "request": request,
            "preselected_venta_id": id_venta,
            "variantes_disponibles": variantes_disponibles,
            "active_menu": "devoluciones",
        }
    )


@router.get("/devoluciones/historial", response_class=HTMLResponse)
def list_devoluciones_historial(
    request: Request,
    page: int = Query(1, ge=1),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    motivo: Optional[str] = None
):
    """Historial de devoluciones con filtros de fecha y motivo."""
    offset = (page - 1) * PAGE_SIZE

    total = DevolucionRepository.count(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        motivo=motivo
    )

    devoluciones = DevolucionRepository.get_all(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        motivo=motivo,
        limit=PAGE_SIZE,
        offset=offset
    )

    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    return templates.TemplateResponse(
        "devoluciones/historial.html",
        {
            "request": request,
            "devoluciones": devoluciones,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "selected_motivo": motivo,
            "active_menu": "devoluciones",
        }
    )


@router.get("/devoluciones/{id_devolucion}", response_class=HTMLResponse)
def ver_detalle_devolucion(request: Request, id_devolucion: int):
    """Vista detallada de una devolución."""
    try:
        devolucion = DevolucionService.obtener_devolucion_completa(id_devolucion)
    except RecordNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Devolución no encontrada.")

    return templates.TemplateResponse(
        "devoluciones/detalle.html",
        {
            "request": request,
            "devolucion": devolucion,
            "active_menu": "devoluciones",
        }
    )


# ============================================================================
# ENDPOINTS REST (JSON)
# ============================================================================

@router.post("/devoluciones")
def registrar_devolucion(datos: DevolucionCreate):
    """Registra una devolución, cambio o reparación ajustando el stock según corresponda."""
    try:
        id_devolucion = DevolucionService.registrar_devolucion(datos)
        return {
            "id_devolucion": id_devolucion,
            "message": f"Devolución #{id_devolucion} procesada exitosamente."
        }
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/api/devoluciones/venta/{id_venta}")
def api_items_venta_devolucion(id_venta: int):
    """Obtiene los renglones de una venta con el saldo disponible para devolver."""
    venta = VentaRepository.get_by_id(id_venta)
    if not venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Venta #{id_venta} no encontrada.")

    items = DevolucionRepository.get_items_venta_disponibles_para_devolucion(id_venta)

    return {
        "id_venta": venta["id_venta"],
        "fecha_hora": venta["fecha_hora"].strftime("%d/%m/%Y %H:%M"),
        "nombre_medio": venta["nombre_medio"],
        "monto_total": float(venta["monto_total"]),
        "items": items
    }
