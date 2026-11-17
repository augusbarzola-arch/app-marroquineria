from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
)


class TamanoRepository:
    """Repositorio para la tabla 'tamano' (sin ñ) usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene tamaños con filtro de búsqueda opcional y paginación."""
        query = "SELECT id_tamano, nombre_tamano FROM tamano"
        params = []

        if search:
            query += " WHERE nombre_tamano ILIKE %s"
            params.append(f"%{search.strip()}%")

        query += " ORDER BY id_tamano ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de tamaños para paginación."""
        query = "SELECT COUNT(*) AS total FROM tamano"
        params = []

        if search:
            query += " WHERE nombre_tamano ILIKE %s"
            params.append(f"%{search.strip()}%")

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_tamano: int) -> Optional[dict]:
        """Obtiene un tamaño por su ID."""
        query = "SELECT id_tamano, nombre_tamano FROM tamano WHERE id_tamano = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_tamano,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_nombre(nombre_tamano: str) -> Optional[dict]:
        """Obtiene un tamaño por su nombre exacto."""
        query = "SELECT id_tamano, nombre_tamano FROM tamano WHERE LOWER(nombre_tamano) = LOWER(%s)"
        with get_db_cursor() as cur:
            cur.execute(query, (nombre_tamano.strip(),))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre_tamano: str) -> int:
        """Inserta un nuevo tamaño y retorna su ID."""
        query = """
            INSERT INTO tamano (nombre_tamano)
            VALUES (%s)
            RETURNING id_tamano
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_tamano.strip(),))
                row = cur.fetchone()
                return row["id_tamano"]
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un tamaño con el nombre '{nombre_tamano.strip()}'.") from e

    @staticmethod
    def update(id_tamano: int, nombre_tamano: str) -> bool:
        """Actualiza el nombre de un tamaño existente."""
        query = """
            UPDATE tamano
            SET nombre_tamano = %s
            WHERE id_tamano = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_tamano.strip(), id_tamano))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Tamaño con ID {id_tamano} no encontrado.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un tamaño con el nombre '{nombre_tamano.strip()}'.") from e

    @staticmethod
    def count_references(id_tamano: int) -> int:
        """Cuenta la cantidad de variantes de productos asociadas a este tamaño."""
        query = "SELECT COUNT(*) AS total FROM variante_producto WHERE id_tamano = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_tamano,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_tamano: int) -> bool:
        """Elimina un tamaño si no tiene variantes dependientes."""
        refs = TamanoRepository.count_references(id_tamano)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} variante(s) de producto.",
                count=refs
            )

        query = "DELETE FROM tamano WHERE id_tamano = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_tamano,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Tamaño con ID {id_tamano} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
