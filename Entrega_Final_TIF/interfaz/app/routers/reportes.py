from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Request, Query, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.services.reporte_service import ReporteService

router = APIRouter(tags=["Reportes y Exportación"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("/reportes", response_class=HTMLResponse)
def vista_reportes(
    request: Request,
    tab: str = Query("ventas_fechas"),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None
):
    """Vista principal de reportes con navegación por pestañas y tablas de resultados."""
    try:
        titulo, columnas, filas, info = ReporteService.obtener_datos_reporte(
            tipo=tab,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
    except ValueError as e:
        # Fallback a ventas_fechas si el tipo es inválido
        tab = "ventas_fechas"
        titulo, columnas, filas, info = ReporteService.obtener_datos_reporte(
            tipo=tab,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )

    return templates.TemplateResponse(
        "reportes/index.html",
        {
            "request": request,
            "active_tab": tab,
            "titulo": titulo,
            "columnas": columnas,
            "filas": filas,
            "info_resumen": info,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "active_menu": "reportes",
        }
    )


@router.get("/reportes/export/csv")
def exportar_reporte_csv(
    tipo: str = Query(...),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None
):
    """Exporta el reporte seleccionado a un archivo CSV codificado con UTF-8 BOM."""
    try:
        _, columnas, filas, _ = ReporteService.obtener_datos_reporte(
            tipo=tipo,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        csv_bytes = ReporteService.exportar_a_csv(columnas, filas)
        nombre_archivo = f"reporte_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

        return Response(
            content=csv_bytes,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={nombre_archivo}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al generar exportación CSV: {e}"
        )


@router.get("/reportes/export/pdf")
def exportar_reporte_pdf(
    tipo: str = Query(...),
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None
):
    """Exporta el reporte seleccionado a un documento PDF mediante ReportLab."""
    try:
        titulo, columnas, filas, info = ReporteService.obtener_datos_reporte(
            tipo=tipo,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        # Orientación horizontal para tablas con muchas columnas
        orientacion_horizontal = tipo in ["stock_valorizado", "compras_proveedor", "top_productos"]

        pdf_bytes = ReporteService.exportar_a_pdf(
            titulo=titulo,
            columnas=columnas,
            filas=filas,
            info_adicional=info,
            horizontal=orientacion_horizontal
        )
        nombre_archivo = f"reporte_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={nombre_archivo}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al generar exportación PDF: {e}"
        )
