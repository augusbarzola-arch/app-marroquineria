from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from app.database import get_db_cursor


class CompraRepository:
    """Repositorio para las tablas 'compra' y 'detalle_compra' usando SQL directo."""

    @staticmethod
    def get_all(
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        id_proveedor: Optional[int] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Historial de compras con filtros de fecha y proveedor."""
        query = """
            SELECT 
                c.id_compra,
                c.fecha_compra,
                c.monto_total,
                c.id_proveedor,
                prov.razon_social,
                prov.cuit,
                COUNT(dc.renglon_compra) AS cantidad_items,
                COALESCE(SUM(dc.cantidad), 0) AS unidades_totales
            FROM compra c
            JOIN proveedor prov ON c.id_proveedor = prov.id_proveedor
            LEFT JOIN detalle_compra dc ON c.id_compra = dc.id_compra
            WHERE 1=1
        """
        params = []

        if fecha_desde:
            query += " AND c.fecha_compra >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND c.fecha_compra <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if id_proveedor:
            query += " AND c.id_proveedor = %s"
            params.append(id_proveedor)

        query += """
            GROUP BY c.id_compra, prov.razon_social, prov.cuit
            ORDER BY c.fecha_compra DESC, c.id_compra DESC
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
        id_proveedor: Optional[int] = None
    ) -> int:
        """Cuenta total de compras registradas para paginación."""
        query = "SELECT COUNT(*) AS total FROM compra c WHERE 1=1"
        params = []

        if fecha_desde:
            query += " AND c.fecha_compra >= %s"
            params.append(f"{fecha_desde} 00:00:00")

        if fecha_hasta:
            query += " AND c.fecha_compra <= %s"
            params.append(f"{fecha_hasta} 23:59:59")

        if id_proveedor:
            query += " AND c.id_proveedor = %s"
            params.append(id_proveedor)

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_compra: int) -> Optional[Dict[str, Any]]:
        """Obtiene la cabecera de una compra y los datos del proveedor."""
        query = """
            SELECT 
                c.id_compra,
                c.fecha_compra,
                c.monto_total,
                c.id_proveedor,
                prov.razon_social,
                prov.cuit,
                prov.telefono,
                prov.email
            FROM compra c
            JOIN proveedor prov ON c.id_proveedor = prov.id_proveedor
            WHERE c.id_compra = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_compra,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_detalles(id_compra: int) -> List[Dict[str, Any]]:
        """Obtiene los renglones de una compra con datos de producto, color y tamaño."""
        query = """
            SELECT 
                dc.id_compra,
                dc.renglon_compra,
                dc.cantidad,
                dc.precio_costo_unitario,
                (dc.cantidad * dc.precio_costo_unitario) AS subtotal,
                dc.id_variante,
                p.id_producto,
                p.nombre_producto,
                p.precio_costo AS precio_costo_referencia,
                col.nombre_color,
                tam.nombre_tamano,
                cat.nombre_categoria
            FROM detalle_compra dc
            JOIN variante_producto v ON dc.id_variante = v.id_variante
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE dc.id_compra = %s
            ORDER BY dc.renglon_compra ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_compra,))
            return [dict(row) for row in cur.fetchall()]
