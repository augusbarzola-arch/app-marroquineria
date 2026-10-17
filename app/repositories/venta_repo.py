from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from app.database import get_db_cursor


class VentaRepository:
    """Repositorio para las tablas 'venta' y 'detalle_venta' usando SQL directo."""

    @staticmethod
    def get_all(
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        id_medio_pago: Optional[int] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Historial de ventas con filtros de fecha, medio de pago y datos agregados."""
        query = """
            SELECT 
                v.id_venta,
                v.fecha_hora,
                v.monto_total,
                v.id_medio_pago,
                mp.nombre_medio,
                mp.porcentaje_descuento_recargo,
                COUNT(dv.renglon_venta) AS cantidad_items,
                COALESCE(SUM(dv.cantidad), 0) AS unidades_totales
            FROM venta v
            JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
            LEFT JOIN detalle_venta dv ON v.id_venta = dv.id_venta
            WHERE 1=1
        """
        params = []

        if fecha_desde:
            query += " AND v.fecha_hora >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND v.fecha_hora <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if id_medio_pago:
            query += " AND v.id_medio_pago = %s"
            params.append(id_medio_pago)

        query += """
            GROUP BY v.id_venta, mp.nombre_medio, mp.porcentaje_descuento_recargo
            ORDER BY v.fecha_hora DESC, v.id_venta DESC
        """

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        id_medio_pago: Optional[int] = None
    ) -> int:
        """Cuenta total de ventas para paginación."""
        query = "SELECT COUNT(*) AS total FROM venta v WHERE 1=1"
        params = []

        if fecha_desde:
            query += " AND v.fecha_hora >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND v.fecha_hora <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if id_medio_pago:
            query += " AND v.id_medio_pago = %s"
            params.append(id_medio_pago)

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_venta: int) -> Optional[Dict[str, Any]]:
        """Obtiene la cabecera de una venta con datos de su medio de pago."""
        query = """
            SELECT 
                v.id_venta,
                v.fecha_hora,
                v.monto_total,
                v.id_medio_pago,
                mp.nombre_medio,
                mp.porcentaje_descuento_recargo
            FROM venta v
            JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
            WHERE v.id_venta = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_venta,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_detalles(id_venta: int) -> List[Dict[str, Any]]:
        """Obtiene los renglones de una venta con descripción del producto, color y tamaño."""
        query = """
            SELECT 
                dv.id_venta,
                dv.renglon_venta,
                dv.cantidad,
                dv.precio_unitario_cobrado,
                (dv.cantidad * dv.precio_unitario_cobrado) AS subtotal,
                dv.id_variante,
                p.id_producto,
                p.nombre_producto,
                p.precio_lista AS precio_lista_original,
                col.nombre_color,
                tam.nombre_tamano,
                cat.nombre_categoria
            FROM detalle_venta dv
            JOIN variante_producto v ON dv.id_variante = v.id_variante
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE dv.id_venta = %s
            ORDER BY dv.renglon_venta ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_venta,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def search_productos_para_pos(query: Optional[str] = None, id_categoria: Optional[int] = None) -> List[Dict[str, Any]]:
        """Búsqueda optimizada de productos y sus variantes con stock disponible para el POS."""
        base_query = """
            SELECT 
                p.id_producto,
                p.nombre_producto,
                p.precio_lista,
                cat.nombre_categoria,
                mat.nombre_material,
                v.id_variante,
                v.stock_actual,
                v.stock_minimo,
                col.nombre_color,
                tam.nombre_tamano
            FROM producto p
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN material mat ON p.id_material = mat.id_material
            JOIN variante_producto v ON p.id_producto = v.id_producto
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE 1=1
        """
        params = []

        if query:
            base_query += " AND (p.nombre_producto ILIKE %s OR col.nombre_color ILIKE %s OR tam.nombre_tamano ILIKE %s)"
            term = f"%{query.strip()}%"
            params.extend([term, term, term])

        if id_categoria:
            base_query += " AND p.id_categoria = %s"
            params.append(id_categoria)

        base_query += " ORDER BY p.nombre_producto ASC, col.nombre_color ASC, tam.nombre_tamano ASC"

        with get_db_cursor() as cur:
            cur.execute(base_query, tuple(params))
            rows = [dict(row) for row in cur.fetchall()]

        # Agrupar variantes por producto para estructurar la respuesta en el frontend
        productos_map = {}
        for r in rows:
            pid = r["id_producto"]
            if pid not in productos_map:
                productos_map[pid] = {
                    "id_producto": pid,
                    "nombre_producto": r["nombre_producto"],
                    "precio_lista": float(r["precio_lista"]),
                    "nombre_categoria": r["nombre_categoria"],
                    "nombre_material": r["nombre_material"],
                    "variantes": []
                }
            productos_map[pid]["variantes"].append({
                "id_variante": r["id_variante"],
                "nombre_color": r["nombre_color"],
                "nombre_tamano": r["nombre_tamano"],
                "stock_actual": r["stock_actual"],
                "stock_minimo": r["stock_minimo"]
            })

        return list(productos_map.values())
