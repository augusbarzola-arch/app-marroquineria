from typing import List, Optional, Dict, Any
from app.database import get_db_cursor


class DevolucionRepository:
    """Repositorio para la tabla 'devolucion' usando SQL directo."""

    @staticmethod
    def get_all(
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        motivo: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Historial de devoluciones con datos de venta, producto devuelto y producto nuevo."""
        query = """
            SELECT 
                d.id_devolucion,
                d.fecha,
                d.id_venta,
                d.id_variante_devuelta,
                d.cantidad,
                d.motivo,
                d.id_variante_nueva,
                d.monto_diferencia,
                d.observaciones,
                -- Producto Devuelto
                p_dev.id_producto AS id_producto_devuelto,
                p_dev.nombre_producto AS prod_devuelto_nombre,
                col_dev.nombre_color AS color_devuelto_nombre,
                tam_dev.nombre_tamano AS tamano_devuelto_nombre,
                -- Producto Nuevo (si fue CAMBIO)
                p_new.id_producto AS id_producto_nuevo,
                p_new.nombre_producto AS prod_nuevo_nombre,
                col_new.nombre_color AS color_nuevo_nombre,
                tam_new.nombre_tamano AS tamano_nuevo_nombre
            FROM devolucion d
            JOIN variante_producto v_dev ON d.id_variante_devuelta = v_dev.id_variante
            JOIN producto p_dev ON v_dev.id_producto = p_dev.id_producto
            JOIN color col_dev ON v_dev.id_color = col_dev.id_color
            JOIN tamano tam_dev ON v_dev.id_tamano = tam_dev.id_tamano
            LEFT JOIN variante_producto v_new ON d.id_variante_nueva = v_new.id_variante
            LEFT JOIN producto p_new ON v_new.id_producto = p_new.id_producto
            LEFT JOIN color col_new ON v_new.id_color = col_new.id_color
            LEFT JOIN tamano tam_new ON v_new.id_tamano = tam_new.id_tamano
            WHERE 1=1
        """
        params = []

        if fecha_desde:
            query += " AND d.fecha >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND d.fecha <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if motivo:
            query += " AND d.motivo = %s"
            params.append(motivo)

        query += " ORDER BY d.fecha DESC, d.id_devolucion DESC"

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
        motivo: Optional[str] = None
    ) -> int:
        """Cuenta total de devoluciones para paginación."""
        query = "SELECT COUNT(*) AS total FROM devolucion d WHERE 1=1"
        params = []

        if fecha_desde:
            query += " AND d.fecha >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND d.fecha <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if motivo:
            query += " AND d.motivo = %s"
            params.append(motivo)

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_devolucion: int) -> Optional[Dict[str, Any]]:
        """Obtiene una devolución detallada por su ID."""
        query = """
            SELECT 
                d.id_devolucion,
                d.fecha,
                d.id_venta,
                d.id_variante_devuelta,
                d.cantidad,
                d.motivo,
                d.id_variante_nueva,
                d.monto_diferencia,
                d.observaciones,
                v.fecha_hora AS fecha_venta_original,
                -- Devuelta
                p_dev.nombre_producto AS prod_devuelto_nombre,
                col_dev.nombre_color AS color_devuelto_nombre,
                tam_dev.nombre_tamano AS tamano_devuelto_nombre,
                -- Nueva
                p_new.nombre_producto AS prod_nuevo_nombre,
                col_new.nombre_color AS color_nuevo_nombre,
                tam_new.nombre_tamano AS tamano_nuevo_nombre
            FROM devolucion d
            JOIN venta v ON d.id_venta = v.id_venta
            JOIN variante_producto v_dev ON d.id_variante_devuelta = v_dev.id_variante
            JOIN producto p_dev ON v_dev.id_producto = p_dev.id_producto
            JOIN color col_dev ON v_dev.id_color = col_dev.id_color
            JOIN tamano tam_dev ON v_dev.id_tamano = tam_dev.id_tamano
            LEFT JOIN variante_producto v_new ON d.id_variante_nueva = v_new.id_variante
            LEFT JOIN producto p_new ON v_new.id_producto = p_new.id_producto
            LEFT JOIN color col_new ON v_new.id_color = col_new.id_color
            LEFT JOIN tamano tam_new ON v_new.id_tamano = tam_new.id_tamano
            WHERE d.id_devolucion = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_devolucion,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_cantidad_ya_devuelta(id_venta: int, id_variante: int) -> int:
        """Obtiene la suma de unidades ya devueltas de esa variante en esa venta."""
        query = """
            SELECT COALESCE(SUM(cantidad), 0) AS total
            FROM devolucion
            WHERE id_venta = %s AND id_variante_devuelta = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_venta, id_variante))
            row = cur.fetchone()
            return int(row["total"]) if row else 0

    @staticmethod
    def get_items_venta_disponibles_para_devolucion(id_venta: int) -> List[Dict[str, Any]]:
        """Obtiene los renglones de una venta calculando el saldo de unidades aún disponibles para devolver."""
        query = """
            SELECT 
                dv.renglon_venta,
                dv.id_variante,
                dv.cantidad AS cantidad_vendida,
                dv.precio_unitario_cobrado,
                p.nombre_producto,
                col.nombre_color,
                tam.nombre_tamano,
                COALESCE((
                    SELECT SUM(d.cantidad)
                    FROM devolucion d
                    WHERE d.id_venta = dv.id_venta AND d.id_variante_devuelta = dv.id_variante
                ), 0) AS cantidad_ya_devuelta
            FROM detalle_venta dv
            JOIN variante_producto v ON dv.id_variante = v.id_variante
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE dv.id_venta = %s
            ORDER BY dv.renglon_venta ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_venta,))
            rows = [dict(row) for row in cur.fetchall()]

        for r in rows:
            r["cantidad_disponible"] = r["cantidad_vendida"] - r["cantidad_ya_devuelta"]

        return rows
