from typing import List, Optional, Dict, Any
from app.database import get_db_cursor


class ReporteRepository:
    """Repositorio para la generación de reportes comerciales y de inventario."""

    @staticmethod
    def ventas_por_fecha(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> Dict[str, Any]:
        """Reporte 1: Ventas por rango de fechas agrupadas por día, con totales y ticket promedio."""
        query = """
            SELECT 
                DATE(v.fecha_hora) AS dia,
                COUNT(v.id_venta) AS cantidad_ventas,
                COALESCE(SUM(v.monto_total), 0) AS total_facturado,
                COALESCE(AVG(v.monto_total), 0) AS ticket_promedio
            FROM venta v
            WHERE (%s::text IS NULL OR v.fecha_hora >= %s::date)
              AND (%s::text IS NULL OR v.fecha_hora <= (%s::date + INTERVAL '1 day' - INTERVAL '1 second'))
            GROUP BY DATE(v.fecha_hora)
            ORDER BY dia DESC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (fecha_desde, fecha_desde, fecha_hasta, fecha_hasta))
            rows = [dict(r) for r in cur.fetchall()]

        total_facturado = sum(r["total_facturado"] for r in rows)
        total_ventas = sum(r["cantidad_ventas"] for r in rows)
        ticket_promedio_general = (total_facturado / total_ventas) if total_ventas > 0 else 0.0

        return {
            "filas": rows,
            "total_facturado": float(total_facturado),
            "total_ventas": int(total_ventas),
            "ticket_promedio_general": float(ticket_promedio_general)
        }

    @staticmethod
    def top_productos_mas_vendidos(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reporte 2: Top 10 de productos más vendidos en un rango de fechas."""
        query = """
            SELECT 
                p.id_producto,
                p.nombre_producto,
                cat.nombre_categoria,
                COALESCE(SUM(dv.cantidad), 0) AS unidades_vendidas,
                COALESCE(SUM(dv.cantidad * dv.precio_unitario_cobrado), 0) AS total_recaudado
            FROM detalle_venta dv
            JOIN venta v ON dv.id_venta = v.id_venta
            JOIN variante_producto vp ON dv.id_variante = vp.id_variante
            JOIN producto p ON vp.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            WHERE (%s::text IS NULL OR v.fecha_hora >= %s::date)
              AND (%s::text IS NULL OR v.fecha_hora <= (%s::date + INTERVAL '1 day' - INTERVAL '1 second'))
            GROUP BY p.id_producto, p.nombre_producto, cat.nombre_categoria
            ORDER BY unidades_vendidas DESC, total_recaudado DESC
            LIMIT 10
        """
        with get_db_cursor() as cur:
            cur.execute(query, (fecha_desde, fecha_desde, fecha_hasta, fecha_hasta))
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def ventas_por_medio_pago(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reporte 3: Cantidad de ventas y monto total agrupado por medio de pago."""
        query = """
            SELECT 
                mp.id_medio_pago,
                mp.nombre_medio,
                mp.porcentaje_descuento_recargo,
                COUNT(v.id_venta) AS cantidad_ventas,
                COALESCE(SUM(v.monto_total), 0) AS monto_total
            FROM medio_pago mp
            LEFT JOIN venta v ON mp.id_medio_pago = v.id_medio_pago
               AND (%s::text IS NULL OR v.fecha_hora >= %s::date)
               AND (%s::text IS NULL OR v.fecha_hora <= (%s::date + INTERVAL '1 day' - INTERVAL '1 second'))
            GROUP BY mp.id_medio_pago, mp.nombre_medio, mp.porcentaje_descuento_recargo
            ORDER BY monto_total DESC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (fecha_desde, fecha_desde, fecha_hasta, fecha_hasta))
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def compras_por_proveedor(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reporte 4: Cantidad de compras y monto total agrupado por proveedor."""
        query = """
            SELECT 
                prov.id_proveedor,
                prov.razon_social,
                prov.cuit,
                COUNT(DISTINCT c.id_compra) AS cantidad_compras,
                COALESCE(SUM(dc.cantidad), 0) AS unidades_compradas,
                COALESCE(SUM(c.monto_total), 0) AS monto_total
            FROM proveedor prov
            LEFT JOIN compra c ON prov.id_proveedor = c.id_proveedor
               AND (%s::text IS NULL OR c.fecha_compra >= %s::date)
               AND (%s::text IS NULL OR c.fecha_compra <= (%s::date + INTERVAL '1 day' - INTERVAL '1 second'))
            LEFT JOIN detalle_compra dc ON c.id_compra = dc.id_compra
            GROUP BY prov.id_proveedor, prov.razon_social, prov.cuit
            ORDER BY monto_total DESC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (fecha_desde, fecha_desde, fecha_hasta, fecha_hasta))
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def devoluciones_por_motivo(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reporte 5: Devoluciones agrupadas por motivo (DEVOLUCION, CAMBIO, REPARACION)."""
        query = """
            SELECT 
                d.motivo,
                COUNT(d.id_devolucion) AS cantidad_devoluciones,
                COALESCE(SUM(d.cantidad), 0) AS unidades_totales,
                COALESCE(SUM(d.monto_diferencia), 0) AS total_diferencia
            FROM devolucion d
            WHERE (%s::text IS NULL OR d.fecha >= %s::date)
              AND (%s::text IS NULL OR d.fecha <= (%s::date + INTERVAL '1 day' - INTERVAL '1 second'))
            GROUP BY d.motivo
            ORDER BY cantidad_devoluciones DESC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (fecha_desde, fecha_desde, fecha_hasta, fecha_hasta))
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def stock_valorizado() -> Dict[str, Any]:
        """Reporte 6: Listado de variantes con su valorización al costo y total general."""
        query = """
            SELECT 
                v.id_variante,
                p.nombre_producto,
                cat.nombre_categoria,
                col.nombre_color,
                tam.nombre_tamano,
                v.stock_actual,
                p.precio_costo,
                (v.stock_actual * p.precio_costo) AS valor_total
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            ORDER BY p.nombre_producto ASC, col.nombre_color ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            rows = [dict(r) for r in cur.fetchall()]

        total_unidades = sum(r["stock_actual"] for r in rows)
        valor_total_general = sum(r["valor_total"] for r in rows)

        return {
            "filas": rows,
            "total_unidades": int(total_unidades),
            "valor_total_general": float(valor_total_general)
        }

    @staticmethod
    def variantes_stock_bajo() -> List[Dict[str, Any]]:
        """Reporte 7: Listado completo de variantes en stock crítico (stock_actual <= stock_minimo)."""
        query = """
            SELECT 
                v.id_variante,
                p.nombre_producto,
                cat.nombre_categoria,
                col.nombre_color,
                tam.nombre_tamano,
                v.stock_actual,
                v.stock_minimo,
                (v.stock_minimo - v.stock_actual) AS faltante_minimo
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE v.stock_actual <= v.stock_minimo
            ORDER BY (v.stock_minimo - v.stock_actual) DESC, v.stock_actual ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query)
            return [dict(r) for r in cur.fetchall()]
