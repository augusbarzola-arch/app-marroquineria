from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import templates
from app.repositories.dashboard_repo import DashboardRepository

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(request: Request):
    """Pantalla principal con métricas clave, alertas de stock, gráfico interactivo y últimas ventas."""
    metricas = DashboardRepository.get_metricas_generales()
    stock_critico = DashboardRepository.get_variantes_stock_critico(limit=8)
    ultimas_ventas = DashboardRepository.get_ultimas_ventas(limit=5)
    ventas_hoy_detalle = DashboardRepository.get_ventas_hoy_detalle(limit=5)
    ventas_mes_medios = DashboardRepository.get_ventas_mes_por_medio()
    estadisticas_ventas = DashboardRepository.get_estadisticas_ventas()
    chart_data = DashboardRepository.get_ventas_ultimos_30_dias()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metricas": metricas,
            "stock_critico": stock_critico,
            "ultimas_ventas": ultimas_ventas,
            "ventas_hoy_detalle": ventas_hoy_detalle,
            "ventas_mes_medios": ventas_mes_medios,
            "estadisticas_ventas": estadisticas_ventas,
            "chart_data": chart_data,
            "active_menu": "dashboard",
        }
    )
