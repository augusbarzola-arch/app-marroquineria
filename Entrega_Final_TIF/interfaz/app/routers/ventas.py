import math
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

from app.templating import templates
from app.database import DatabaseError, RecordNotFoundError
from app.models.venta import VentaCreate
from app.repositories.venta_repo import VentaRepository
from app.repositories.categoria_repo import CategoriaRepository
from app.repositories.medio_pago_repo import MedioPagoRepository
from app.services.venta_service import VentaService

router = APIRouter(tags=["Gestión de Ventas"])
PAGE_SIZE = 15


# ============================================================================
# VISTAS HTML
# ============================================================================

@router.get("/ventas/pos", response_class=HTMLResponse)
def pos_interface(request: Request):
    """Interfaz del Punto de Venta (POS) en 3 paneles."""
    categorias = CategoriaRepository.get_all()
    medios_pago = MedioPagoRepository.get_all()
    return templates.TemplateResponse(
        "ventas/pos.html",
        {
            "request": request,
            "categorias": categorias,
            "medios_pago": medios_pago,
            "active_menu": "ventas",
        }
    )


@router.get("/ventas/historial", response_class=HTMLResponse)
def list_ventas_historial(
    request: Request,
    page: int = Query(1, ge=1),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    id_medio_pago: Optional[int] = None
):
    """Historial de ventas con filtros de fecha y medio de pago."""
    offset = (page - 1) * PAGE_SIZE

    total = VentaRepository.count(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        id_medio_pago=id_medio_pago
    )

    ventas = VentaRepository.get_all(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        id_medio_pago=id_medio_pago,
        limit=PAGE_SIZE,
        offset=offset
    )

    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1
    medios_pago = MedioPagoRepository.get_all()

    return templates.TemplateResponse(
        "ventas/historial.html",
        {
            "request": request,
            "ventas": ventas,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "selected_medio_pago": id_medio_pago,
            "medios_pago": medios_pago,
            "active_menu": "ventas_historial",
        }
    )


@router.get("/ventas/{id_venta}/comprobante", response_class=HTMLResponse)
def ver_comprobante_venta(request: Request, id_venta: int):
    """Comprobante interno no fiscal imprimible con window.print()."""
    try:
        data = VentaService.obtener_venta_completa(id_venta)
    except RecordNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    return templates.TemplateResponse(
        "ventas/comprobante.html",
        {
            "request": request,
            "venta": data["venta"],
            "detalles": data["detalles"],
            "subtotal_original": data["subtotal_original"],
            "descuento_recargo_monto": data["descuento_recargo_monto"],
            "total_unidades": data["total_unidades"],
            "active_menu": "ventas_historial",
        }
    )


@router.get("/ventas/{id_venta}", response_class=HTMLResponse)
def ver_detalle_venta(request: Request, id_venta: int):
    """Vista detallada de una venta y sus renglones."""
    try:
        data = VentaService.obtener_venta_completa(id_venta)
    except RecordNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

    return templates.TemplateResponse(
        "ventas/detalle.html",
        {
            "request": request,
            "venta": data["venta"],
            "detalles": data["detalles"],
            "subtotal_original": data["subtotal_original"],
            "descuento_recargo_monto": data["descuento_recargo_monto"],
            "total_unidades": data["total_unidades"],
            "active_menu": "ventas_historial",
        }
    )


# ============================================================================
# ENDPOINTS REST (JSON)
# ============================================================================

@router.post("/ventas")
def registrar_venta(datos: VentaCreate):
    """Procesa y asienta una venta en una única transacción atómica."""
    try:
        id_venta = VentaService.registrar_venta(datos)
        return {
            "id_venta": id_venta,
            "message": f"Venta #{id_venta} registrada exitosamente."
        }
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/api/ventas/buscar-productos")
def api_buscar_productos(
    query: Optional[str] = None,
    id_categoria: Optional[int] = None
):
    """Buscador en tiempo real de productos y variantes para el POS."""
    return VentaRepository.search_productos_para_pos(query=query, id_categoria=id_categoria)
