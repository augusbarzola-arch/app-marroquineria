from typing import Dict, Any, List
from app.database import get_db_cursor


class DashboardRepository:
    """Repositorio para consultas analíticas y agregadas del Dashboard."""

    @staticmethod
    def get_metricas_generales() -> Dict[str, Any]:
        """Obtiene las 4 métricas clave: ventas hoy, ventas del mes, ticket promedio y stock crítico."""
        query = """
            SELECT
                -- Ventas de hoy
                COALESCE(SUM(CASE WHEN DATE(fecha_hora) = CURRENT_DATE THEN monto_total ELSE 0 END), 0) AS ventas_hoy_monto,
                COUNT(CASE WHEN DATE(fecha_hora) = CURRENT_DATE THEN 1 END) AS ventas_hoy_cantidad,
                
                -- Ventas del mes actual
                COALESCE(SUM(CASE WHEN DATE_TRUNC('month', fecha_hora) = DATE_TRUNC('month', CURRENT_DATE) THEN monto_total ELSE 0 END), 0) AS ventas_mes_monto,
                COUNT(CASE WHEN DATE_TRUNC('month', fecha_hora) = DATE_TRUNC('month', CURRENT_DATE) THEN 1 END) AS ventas_mes_cantidad,
                
                -- Ticket promedio histórico
                COALESCE(AVG(monto_total), 0) AS ticket_promedio
            FROM venta;
        """
        stock_query = """
            SELECT COUNT(*) AS total_stock_bajo
            FROM variante_producto
            WHERE stock_actual <= stock_minimo;
        """

        with get_db_cursor() as cur:
            cur.execute(query)
            row_v = cur.fetchone() or {}

            cur.execute(stock_query)
            row_s = cur.fetchone() or {}

            # Si el mes actual no tiene ventas (ej: base con datos de prueba de meses anteriores),
            # calculamos el ticket promedio global o del último mes con actividad para que sea informativo.
            ticket_promedio = float(row_v.get("ticket_promedio", 0.0))

            return {
                "ventas_hoy_monto": float(row_v.get("ventas_hoy_monto", 0.0)),
                "ventas_hoy_cantidad": int(row_v.get("ventas_hoy_cantidad", 0)),
                "ventas_mes_monto": float(row_v.get("ventas_mes_monto", 0.0)),
                "ventas_mes_cantidad": int(row_v.get("ventas_mes_cantidad", 0)),
                "ticket_promedio": ticket_promedio,
                "total_stock_bajo": int(row_s.get("total_stock_bajo", 0))
            }

    @staticmethod
    def get_variantes_stock_critico(limit: int = 8) -> List[Dict[str, Any]]:
        """Obtiene las variantes cuyo stock_actual <= stock_minimo con nombres legibles."""
        query = """
            SELECT 
                v.id_variante,
                v.id_producto,
                v.stock_actual,
                v.stock_minimo,
                p.nombre_producto,
                p.precio_lista,
                col.nombre_color,
                tam.nombre_tamano,
                cat.nombre_categoria
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE v.stock_actual <= v.stock_minimo
            ORDER BY (v.stock_minimo - v.stock_actual) DESC, v.stock_actual ASC
            LIMIT %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (limit,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_ultimas_ventas(limit: int = 5) -> List[Dict[str, Any]]:
        """Obtiene las últimas 5 ventas registradas con su medio de pago."""
        query = """
            SELECT 
                v.id_venta,
                v.fecha_hora,
                v.monto_total,
                mp.nombre_medio,
                COUNT(dv.renglon_venta) AS total_items
            FROM venta v
            JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
            LEFT JOIN detalle_venta dv ON v.id_venta = dv.id_venta
            GROUP BY v.id_venta, mp.nombre_medio
            ORDER BY v.fecha_hora DESC, v.id_venta DESC
            LIMIT %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (limit,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_ventas_ultimos_30_dias() -> List[Dict[str, Any]]:
        """Serie temporal de ventas de los últimos 30 días para el gráfico de líneas Chart.js."""
        query = """
            WITH fecha_referencia AS (
                -- Toma el día actual o la fecha más reciente de venta para asegurar datos visibles en el gráfico
                SELECT GREATEST(CURRENT_DATE, COALESCE(MAX(DATE(fecha_hora)), CURRENT_DATE)) AS fecha_fin
                FROM venta
            )
            SELECT 
                d::date AS dia,
                COALESCE(SUM(v.monto_total), 0) AS total_monto,
                COUNT(v.id_venta) AS cantidad_ventas
            FROM fecha_referencia fr,
            generate_series(fr.fecha_fin - INTERVAL '29 days', fr.fecha_fin, '1 day'::interval) d
            LEFT JOIN venta v ON DATE(v.fecha_hora) = d::date
            GROUP BY d::date
            ORDER BY d::date ASC;
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                {
                    "fecha": row["dia"].strftime("%d/%m"),
                    "fecha_completa": row["dia"].strftime("%Y-%m-%d"),
                    "total": float(row["total_monto"]),
                    "cantidad": int(row["cantidad_ventas"])
                }
                for row in rows
            ]

    @staticmethod
    def get_ventas_hoy_detalle(limit: int = 5) -> List[Dict[str, Any]]:
        """Obtiene las ventas ocurridas en el día de hoy."""
        query = """
            SELECT 
                v.id_venta,
                v.fecha_hora,
                v.monto_total,
                mp.nombre_medio,
                COUNT(dv.renglon_venta) AS total_items
            FROM venta v
            JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
            LEFT JOIN detalle_venta dv ON v.id_venta = dv.id_venta
            WHERE DATE(v.fecha_hora) = CURRENT_DATE
            GROUP BY v.id_venta, mp.nombre_medio
            ORDER BY v.fecha_hora DESC, v.id_venta DESC
            LIMIT %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (limit,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_ventas_mes_por_medio() -> List[Dict[str, Any]]:
        """Distribución de cobros del mes agrupado por medio de pago."""
        query = """
            SELECT 
                mp.nombre_medio,
                COUNT(v.id_venta) AS cantidad,
                COALESCE(SUM(v.monto_total), 0) AS total
            FROM venta v
            JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
            WHERE DATE_TRUNC('month', v.fecha_hora) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY mp.nombre_medio
            ORDER BY total DESC;
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            return [
                {
                    "nombre_medio": row["nombre_medio"],
                    "cantidad": int(row["cantidad"]),
                    "total": float(row["total"])
                }
                for row in cur.fetchall()
            ]

    @staticmethod
    def get_estadisticas_ventas() -> Dict[str, Any]:
        """Estadísticas avanzadas para la tarjeta de ticket promedio."""
        query = """
            SELECT 
                COALESCE(MAX(monto_total), 0) AS venta_maxima,
                COALESCE(MIN(monto_total), 0) AS venta_minima,
                COUNT(*) AS total_ventas,
                COALESCE(SUM(monto_total), 0) AS total_facturado
            FROM venta;
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            row = cur.fetchone() or {}
            return {
                "venta_maxima": float(row.get("venta_maxima", 0.0)),
                "venta_minima": float(row.get("venta_minima", 0.0)),
                "total_ventas": int(row.get("total_ventas", 0)),
                "total_facturado": float(row.get("total_facturado", 0.0))
            }

