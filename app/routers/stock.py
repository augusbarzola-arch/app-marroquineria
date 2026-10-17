import math
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

from app.templating import templates
from app.query_params import OptionalIntQuery, OptionalStrQuery, BoolQuery
from app.database import DatabaseError, RecordNotFoundError
from app.models.variante import VarianteStockQuickUpdate
from app.repositories.variante_repo import VarianteRepository
from app.repositories.producto_repo import ProductoRepository
from app.repositories.color_repo import ColorRepository
from app.repositories.tamano_repo import TamanoRepository
from app.services.stock_service import StockService

router = APIRouter(tags=["Gestión de Stock y Variantes"])
PAGE_SIZE = 15


@router.get("/stock", response_class=HTMLResponse)
def list_stock(
    request: Request,
    page: int = Query(1, ge=1),
    search: OptionalStrQuery = None,
    id_producto: OptionalIntQuery = None,
    id_color: OptionalIntQuery = None,
    id_tamano: OptionalIntQuery = None,
    solo_stock_bajo: BoolQuery = False
):
    """Listado general de variantes con filtros avanzados y edición en línea de stock."""
    # Selects "Todos" envían "" y no deben romperse como int inválido.
    offset = (page - 1) * PAGE_SIZE

    total = VarianteRepository.count_variantes(
        search=search,
        id_producto=id_producto,
        id_color=id_color,
        id_tamano=id_tamano,
        solo_stock_bajo=solo_stock_bajo
    )

    variantes = StockService.listar_variantes(
        search=search,
        id_producto=id_producto,
        id_color=id_color,
        id_tamano=id_tamano,
        solo_stock_bajo=solo_stock_bajo,
        limit=PAGE_SIZE,
        offset=offset
    )

    total_pages = math.ceil(total / PAGE_SIZE) if total > 0 else 1

    productos = ProductoRepository.get_all()
    colores = ColorRepository.get_all()
    tamanos = TamanoRepository.get_all()
    resumen = StockService.obtener_resumen_inventario()

    return templates.TemplateResponse(
        "stock/listado.html",
        {
            "request": request,
            "variantes": variantes,
            "total": total,
            "current_page": page,
            "total_pages": total_pages,
            "search": search,
            "selected_producto": id_producto,
            "selected_color": id_color,
            "selected_tamano": id_tamano,
            "solo_stock_bajo": solo_stock_bajo,
            "productos": productos,
            "colores": colores,
            "tamanos": tamanos,
            "resumen": resumen,
            "active_menu": "stock",
        }
    )


@router.put("/stock/{id_variante}")
def update_stock_quick(id_variante: int, datos: VarianteStockQuickUpdate):
    """Actualización rápida en línea de stock_actual y stock_minimo."""
    try:
        resultado = StockService.actualizar_stock_en_linea(
            id_variante=id_variante,
            stock_actual=datos.stock_actual,
            stock_minimo=datos.stock_minimo
        )
        return resultado
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/api/stock/resumen")
def api_stock_resumen():
    """Retorna métricas generales de inventario."""
    return StockService.obtener_resumen_inventario()
