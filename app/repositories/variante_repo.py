from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, CheckViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
    DatabaseError,
)


class VarianteRepository:
    """Repositorio para la tabla 'variante_producto' usando SQL directo."""

    @staticmethod
    def get_all_variantes(
        search: Optional[str] = None,
        id_producto: Optional[int] = None,
        id_color: Optional[int] = None,
        id_tamano: Optional[int] = None,
        solo_stock_bajo: bool = False,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene variantes con filtros cruzados de producto, color, tamaño y stock bajo."""
        query = """
            SELECT 
                v.id_variante,
                v.id_producto,
                v.id_color,
                v.id_tamano,
                v.stock_actual,
                v.stock_minimo,
                p.nombre_producto,
                p.precio_costo,
                p.precio_lista,
                col.nombre_color,
                tam.nombre_tamano,
                cat.nombre_categoria
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN categoria cat ON p.id_categoria = cat.id_categoria
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (p.nombre_producto ILIKE %s OR col.nombre_color ILIKE %s OR tam.nombre_tamano ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        if id_producto:
            query += " AND v.id_producto = %s"
            params.append(id_producto)

        if id_color:
            query += " AND v.id_color = %s"
            params.append(id_color)

        if id_tamano:
            query += " AND v.id_tamano = %s"
            params.append(id_tamano)

        if solo_stock_bajo:
            query += " AND v.stock_actual <= v.stock_minimo"

        query += " ORDER BY (v.stock_actual <= v.stock_minimo) DESC, p.nombre_producto ASC, col.nombre_color ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count_variantes(
        search: Optional[str] = None,
        id_producto: Optional[int] = None,
        id_color: Optional[int] = None,
        id_tamano: Optional[int] = None,
        solo_stock_bajo: bool = False
    ) -> int:
        """Cuenta total de variantes que cumplen con los filtros para paginación."""
        query = """
            SELECT COUNT(*) AS total
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (p.nombre_producto ILIKE %s OR col.nombre_color ILIKE %s OR tam.nombre_tamano ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        if id_producto:
            query += " AND v.id_producto = %s"
            params.append(id_producto)

        if id_color:
            query += " AND v.id_color = %s"
            params.append(id_color)

        if id_tamano:
            query += " AND v.id_tamano = %s"
            params.append(id_tamano)

        if solo_stock_bajo:
            query += " AND v.stock_actual <= v.stock_minimo"

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_variante: int) -> Optional[dict]:
        """Obtiene una variante específica por ID con detalles del producto, color y tamaño."""
        query = """
            SELECT 
                v.id_variante,
                v.id_producto,
                v.id_color,
                v.id_tamano,
                v.stock_actual,
                v.stock_minimo,
                p.nombre_producto,
                p.precio_costo,
                p.precio_lista,
                col.nombre_color,
                tam.nombre_tamano
            FROM variante_producto v
            JOIN producto p ON v.id_producto = p.id_producto
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE v.id_variante = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_variante,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(
        id_producto: int,
        id_color: int,
        id_tamano: int,
        stock_actual: int = 0,
        stock_minimo: int = 0
    ) -> int:
        """Crea una variante garantizando unicidad de (id_producto, id_color, id_tamano)."""
        query = """
            INSERT INTO variante_producto (id_producto, id_color, id_tamano, stock_actual, stock_minimo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_variante
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_producto, id_color, id_tamano, stock_actual, stock_minimo))
                row = cur.fetchone()
                return row["id_variante"]
        except UniqueViolation as e:
            raise UniqueConstraintError(
                "Ya existe una variante con esa combinación exacta de color y tamaño para este producto."
            ) from e
        except CheckViolation as e:
            raise DatabaseError("El stock actual y el stock mínimo deben ser números positivos o cero.") from e

    @staticmethod
    def update(
        id_variante: int,
        id_color: int,
        id_tamano: int,
        stock_actual: int,
        stock_minimo: int
    ) -> bool:
        """Actualiza color, tamaño y stock de una variante."""
        query = """
            UPDATE variante_producto
            SET id_color = %s,
                id_tamano = %s,
                stock_actual = %s,
                stock_minimo = %s
            WHERE id_variante = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_color, id_tamano, stock_actual, stock_minimo, id_variante))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Variante con ID {id_variante} no encontrada.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(
                "Ya existe una variante con esa combinación de color y tamaño para este producto."
            ) from e
        except CheckViolation as e:
            raise DatabaseError("El stock actual y el stock mínimo deben ser mayores o iguales a cero.") from e

    @staticmethod
    def update_stock(id_variante: int, stock_actual: int, stock_minimo: int) -> bool:
        """Actualiza exclusivamente el stock de la variante (para edición rápida en línea)."""
        query = """
            UPDATE variante_producto
            SET stock_actual = %s, stock_minimo = %s
            WHERE id_variante = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (stock_actual, stock_minimo, id_variante))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Variante con ID {id_variante} no encontrada.")
                return True
        except CheckViolation as e:
            raise DatabaseError("El stock no puede ser negativo.") from e

    @staticmethod
    def count_references(id_variante: int) -> int:
        """Cuenta el uso de esta variante en detalles de ventas, compras o devoluciones."""
        query = """
            SELECT (
                (SELECT COUNT(*) FROM detalle_venta WHERE id_variante = %s) +
                (SELECT COUNT(*) FROM detalle_compra WHERE id_variante = %s) +
                (SELECT COUNT(*) FROM devolucion WHERE id_variante_devuelta = %s OR id_variante_nueva = %s)
            ) AS total
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_variante, id_variante, id_variante, id_variante))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_variante: int) -> bool:
        """Elimina una variante si no tiene movimientos asociados."""
        refs = VarianteRepository.count_references(id_variante)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar la variante porque está registrada en {refs} movimiento(s) comercial(es).",
                count=refs
            )

        query = "DELETE FROM variante_producto WHERE id_variante = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_variante,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Variante con ID {id_variante} no encontrada.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciada por otros registros.",
                count=refs
            ) from e
