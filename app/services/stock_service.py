import logging
from typing import List, Dict, Any, Optional
from app.repositories.variante_repo import VarianteRepository
from app.database import get_db_cursor, DatabaseError, RecordNotFoundError

logger = logging.getLogger("app.services.stock")


class StockService:
    """Servicio para la gestión y control de inventario de variantes."""

    @staticmethod
    def listar_variantes(
        search: Optional[str] = None,
        id_producto: Optional[int] = None,
        id_color: Optional[int] = None,
        id_tamano: Optional[int] = None,
        solo_stock_bajo: bool = False,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Obtiene las variantes calculando su estado de stock (Crítico, Alerta o Normal)."""
        variantes = VarianteRepository.get_all_variantes(
            search=search,
            id_producto=id_producto,
            id_color=id_color,
            id_tamano=id_tamano,
            solo_stock_bajo=solo_stock_bajo,
            limit=limit,
            offset=offset
        )

        for v in variantes:
            actual = v["stock_actual"]
            minimo = v["stock_minimo"]
            if actual <= minimo:
                v["estado_codigo"] = "critico"
                v["estado_nombre"] = "Stock Bajo"
                v["badge_class"] = "bg-danger"
                v["row_class"] = "row-stock-critical"
            elif actual <= (minimo * 1.5):
                v["estado_codigo"] = "alerta"
                v["estado_nombre"] = "Reposición Cercana"
                v["badge_class"] = "bg-warning text-dark"
                v["row_class"] = "row-stock-warning"
            else:
                v["estado_codigo"] = "normal"
                v["estado_nombre"] = "Óptimo"
                v["badge_class"] = "bg-success-subtle text-success-emphasis border"
                v["row_class"] = ""

        return variantes

    @staticmethod
    def actualizar_stock_en_linea(id_variante: int, stock_actual: int, stock_minimo: int) -> Dict[str, Any]:
        """Actualiza stock_actual y stock_minimo directamente desde la tabla."""
        if stock_actual < 0 or stock_minimo < 0:
            raise DatabaseError("El stock actual y el stock mínimo deben ser mayores o iguales a 0.")

        VarianteRepository.update_stock(id_variante, stock_actual, stock_minimo)
        variante = VarianteRepository.get_by_id(id_variante)
        if not variante:
            raise RecordNotFoundError(f"Variante con ID {id_variante} no encontrada.")

        # Calcular nuevo estado
        if stock_actual <= stock_minimo:
            estado_codigo = "critico"
            estado_nombre = "Stock Bajo"
            badge_class = "bg-danger"
            row_class = "row-stock-critical"
        elif stock_actual <= (stock_minimo * 1.5):
            estado_codigo = "alerta"
            estado_nombre = "Reposición Cercana"
            badge_class = "bg-warning text-dark"
            row_class = "row-stock-warning"
        else:
            estado_codigo = "normal"
            estado_nombre = "Óptimo"
            badge_class = "bg-success-subtle text-success-emphasis border"
            row_class = ""

        return {
            "id_variante": id_variante,
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "estado_codigo": estado_codigo,
            "estado_nombre": estado_nombre,
            "badge_class": badge_class,
            "row_class": row_class,
            "message": "Stock actualizado exitosamente."
        }

    @staticmethod
    def obtener_resumen_inventario() -> Dict[str, int]:
        """Retorna estadísticas generales del inventario para tarjetas informativas."""
        query = """
            SELECT 
                COUNT(*) AS total_variantes,
                COALESCE(SUM(stock_actual), 0) AS total_unidades,
                COUNT(CASE WHEN stock_actual <= stock_minimo THEN 1 END) AS total_critico,
                COUNT(CASE WHEN stock_actual > stock_minimo AND stock_actual <= (stock_minimo * 1.5) THEN 1 END) AS total_alerta
            FROM variante_producto
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if row:
                return {
                    "total_variantes": int(row["total_variantes"]),
                    "total_unidades": int(row["total_unidades"]),
                    "total_critico": int(row["total_critico"]),
                    "total_alerta": int(row["total_alerta"])
                }
            return {
                "total_variantes": 0,
                "total_unidades": 0,
                "total_critico": 0,
                "total_alerta": 0
            }
