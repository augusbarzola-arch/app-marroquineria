import json
from decimal import Decimal
from typing import List, Optional, Dict, Any
from app.database import get_db_cursor


class EcommerceRepository:
    """Acceso a datos SQL para el catálogo web, imágenes, pedidos y webhooks."""

    @staticmethod
    def get_productos_tienda(
        id_categoria: Optional[int] = None,
        search: Optional[str] = None,
        limit: int = 24,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Listado público de productos con stock total disponible y fotos."""
        query = """
            SELECT 
                p.id_producto,
                p.sku,
                p.nombre_producto,
                p.descripcion,
                p.precio_lista AS precio_base,
                cat.id_categoria,
                cat.nombre_categoria,
                mat.nombre_material,
                COALESCE(SUM(v.stock_actual), 0) AS stock_total,
                (
                    SELECT pi.url_imagen 
                    FROM producto_imagen pi 
                    WHERE pi.id_producto = p.id_producto 
                    ORDER BY pi.es_portada DESC, pi.orden ASC, pi.id_imagen ASC 
                    LIMIT 1
                ) AS imagen_portada
            FROM producto p
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN material mat ON p.id_material = mat.id_material
            LEFT JOIN variante_producto v ON p.id_producto = v.id_producto
            WHERE 1=1
        """
        params = []

        if id_categoria:
            query += " AND p.id_categoria = %s"
            params.append(id_categoria)

        if search:
            query += " AND (p.nombre_producto ILIKE %s OR p.descripcion ILIKE %s OR p.sku ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        query += """
            GROUP BY p.id_producto, cat.id_categoria, cat.nombre_categoria, mat.nombre_material
            ORDER BY stock_total DESC, p.id_producto DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count_productos_tienda(
        id_categoria: Optional[int] = None,
        search: Optional[str] = None
    ) -> int:
        """Cuenta total de productos públicos para paginación."""
        query = """
            SELECT COUNT(DISTINCT p.id_producto) AS total
            FROM producto p
            WHERE 1=1
        """
        params = []
        if id_categoria:
            query += " AND p.id_categoria = %s"
            params.append(id_categoria)
        if search:
            query += " AND (p.nombre_producto ILIKE %s OR p.descripcion ILIKE %s OR p.sku ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_producto_detalle(id_producto: int) -> Optional[Dict[str, Any]]:
        """Obtiene la ficha técnica completa del producto, sus variantes con stock y su galería."""
        prod_query = """
            SELECT 
                p.id_producto,
                p.sku,
                p.nombre_producto,
                p.descripcion,
                p.precio_lista AS precio_base,
                cat.id_categoria,
                cat.nombre_categoria,
                mat.nombre_material
            FROM producto p
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN material mat ON p.id_material = mat.id_material
            WHERE p.id_producto = %s
        """
        with get_db_cursor() as cur:
            cur.execute(prod_query, (id_producto,))
            prod = cur.fetchone()
            if not prod:
                return None
            prod = dict(prod)

            # Obtener galería de fotos
            cur.execute("""
                SELECT id_imagen, url_imagen, es_portada, orden
                FROM producto_imagen
                WHERE id_producto = %s
                ORDER BY es_portada DESC, orden ASC, id_imagen ASC
            """, (id_producto,))
            prod["imagenes"] = [dict(r) for r in cur.fetchall()]

            # Obtener variantes disponibles con stock
            cur.execute("""
                SELECT 
                    v.id_variante,
                    v.id_color,
                    col.nombre_color,
                    v.id_tamano,
                    tam.nombre_tamano,
                    v.stock_actual,
                    v.stock_minimo
                FROM variante_producto v
                JOIN color col ON v.id_color = col.id_color
                JOIN tamano tam ON v.id_tamano = tam.id_tamano
                WHERE v.id_producto = %s
                ORDER BY col.nombre_color ASC, tam.nombre_tamano ASC
            """, (id_producto,))
            prod["variantes"] = [dict(r) for r in cur.fetchall()]
            prod["stock_total"] = sum(v["stock_actual"] for v in prod["variantes"])

            return prod

    @staticmethod
    def get_pedido_by_id(id_pedido: int) -> Optional[Dict[str, Any]]:
        """Obtiene la cabecera y renglones de un pedido web."""
        with get_db_cursor() as cur:
            cur.execute("SELECT * FROM pedido_web WHERE id_pedido = %s", (id_pedido,))
            ped = cur.fetchone()
            if not ped:
                return None
            pedido = dict(ped)

            cur.execute("""
                SELECT 
                    dp.renglon,
                    dp.id_variante,
                    dp.cantidad,
                    dp.precio_unitario_cobrado,
                    dp.subtotal,
                    p.nombre_producto,
                    p.sku,
                    col.nombre_color,
                    tam.nombre_tamano,
                    (
                        SELECT pi.url_imagen 
                        FROM producto_imagen pi 
                        WHERE pi.id_producto = p.id_producto 
                        ORDER BY pi.es_portada DESC, pi.orden ASC 
                        LIMIT 1
                    ) AS imagen_url
                FROM detalle_pedido_web dp
                JOIN variante_producto v ON dp.id_variante = v.id_variante
                JOIN producto p ON v.id_producto = p.id_producto
                JOIN color col ON v.id_color = col.id_color
                JOIN tamano tam ON v.id_tamano = tam.id_tamano
                WHERE dp.id_pedido = %s
                ORDER BY dp.renglon ASC
            """, (id_pedido,))
            pedido["detalles"] = [dict(r) for r in cur.fetchall()]
            return pedido

    @staticmethod
    def get_pedido_by_codigo(codigo: str) -> Optional[Dict[str, Any]]:
        """Busca pedido por su código único de seguimiento (ej: WEB-2026-0001)."""
        with get_db_cursor() as cur:
            cur.execute("SELECT id_pedido FROM pedido_web WHERE codigo_seguimiento = %s", (codigo,))
            row = cur.fetchone()
            if not row:
                return None
            return EcommerceRepository.get_pedido_by_id(row["id_pedido"])

    @staticmethod
    def get_pedidos(
        estado: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Listado de pedidos web para el panel de administración."""
        query = """
            SELECT 
                pw.*,
                COUNT(dp.renglon) AS cantidad_items,
                COALESCE(SUM(dp.cantidad), 0) AS unidades_totales
            FROM pedido_web pw
            LEFT JOIN detalle_pedido_web dp ON pw.id_pedido = dp.id_pedido
            WHERE 1=1
        """
        params = []
        if estado:
            query += " AND pw.estado = %s"
            params.append(estado)
        if search:
            query += " AND (pw.codigo_seguimiento ILIKE %s OR pw.nombre_cliente ILIKE %s OR pw.email_cliente ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        query += """
            GROUP BY pw.id_pedido
            ORDER BY pw.fecha_creacion DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(r) for r in cur.fetchall()]

    @staticmethod
    def count_pedidos(estado: Optional[str] = None, search: Optional[str] = None) -> int:
        query = "SELECT COUNT(*) AS total FROM pedido_web WHERE 1=1"
        params = []
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        if search:
            query += " AND (codigo_seguimiento ILIKE %s OR nombre_cliente ILIKE %s OR email_cliente ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def guardar_imagen(id_producto: int, url_imagen: str, es_portada: bool = False, orden: int = 0) -> int:
        query = """
            INSERT INTO producto_imagen (id_producto, url_imagen, es_portada, orden)
            VALUES (%s, %s, %s, %s)
            RETURNING id_imagen
        """
        with get_db_cursor(commit=True) as cur:
            cur.execute(query, (id_producto, url_imagen, es_portada, orden))
            return cur.fetchone()["id_imagen"]

    @staticmethod
    def eliminar_imagen(id_imagen: int) -> bool:
        query = "DELETE FROM producto_imagen WHERE id_imagen = %s RETURNING id_imagen"
        with get_db_cursor(commit=True) as cur:
            cur.execute(query, (id_imagen,))
            return cur.fetchone() is not None

    @staticmethod
    def guardar_webhook_log(id_evento: str, tipo_evento: str, payload: dict) -> None:
        """Registra el evento de webhook procesado para garantizar idempotencia."""
        query = """
            INSERT INTO mp_webhook_log (id_evento, tipo_evento, payload)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_evento) DO NOTHING
        """
        with get_db_cursor(commit=True) as cur:
            cur.execute(query, (id_evento, tipo_evento, json.dumps(payload)))

    @staticmethod
    def existe_webhook_log(id_evento: str) -> bool:
        query = "SELECT 1 FROM mp_webhook_log WHERE id_evento = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_evento,))
            return cur.fetchone() is not None
