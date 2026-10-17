from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
)


class ColorRepository:
    """Repositorio para la tabla 'color' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene colores con filtro de búsqueda opcional y paginación."""
        query = "SELECT id_color, nombre_color FROM color"
        params = []

        if search:
            query += " WHERE nombre_color ILIKE %s"
            params.append(f"%{search.strip()}%")

        query += " ORDER BY id_color ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de colores para paginación."""
        query = "SELECT COUNT(*) AS total FROM color"
        params = []

        if search:
            query += " WHERE nombre_color ILIKE %s"
            params.append(f"%{search.strip()}%")

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_color: int) -> Optional[dict]:
        """Obtiene un color por su ID."""
        query = "SELECT id_color, nombre_color FROM color WHERE id_color = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_color,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_nombre(nombre_color: str) -> Optional[dict]:
        """Obtiene un color por su nombre exacto (case-insensitive)."""
        query = "SELECT id_color, nombre_color FROM color WHERE LOWER(nombre_color) = LOWER(%s)"
        with get_db_cursor() as cur:
            cur.execute(query, (nombre_color.strip(),))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre_color: str) -> int:
        """Inserta un nuevo color y retorna su ID."""
        query = """
            INSERT INTO color (nombre_color)
            VALUES (%s)
            RETURNING id_color
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_color.strip(),))
                row = cur.fetchone()
                return row["id_color"]
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un color con el nombre '{nombre_color.strip()}'.") from e

    @staticmethod
    def update(id_color: int, nombre_color: str) -> bool:
        """Actualiza el nombre de un color existente."""
        query = """
            UPDATE color
            SET nombre_color = %s
            WHERE id_color = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_color.strip(), id_color))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Color con ID {id_color} no encontrado.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un color con el nombre '{nombre_color.strip()}'.") from e

    @staticmethod
    def count_references(id_color: int) -> int:
        """Cuenta la cantidad de variantes de productos asociadas a este color."""
        query = "SELECT COUNT(*) AS total FROM variante_producto WHERE id_color = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_color,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_color: int) -> bool:
        """Elimina un color si no tiene variantes dependientes."""
        refs = ColorRepository.count_references(id_color)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} variante(s) de producto.",
                count=refs
            )

        query = "DELETE FROM color WHERE id_color = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_color,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Color con ID {id_color} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
