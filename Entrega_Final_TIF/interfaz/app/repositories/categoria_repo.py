from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
)


class CategoriaRepository:
    """Repositorio para la tabla 'categoria' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene categorías con filtro de búsqueda opcional y paginación."""
        query = "SELECT id_categoria, nombre_categoria, descripcion FROM categoria"
        params = []

        if search:
            query += " WHERE nombre_categoria ILIKE %s OR descripcion ILIKE %s"
            term = f"%{search.strip()}%"
            params.extend([term, term])

        query += " ORDER BY id_categoria ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de categorías (usado para paginación)."""
        query = "SELECT COUNT(*) AS total FROM categoria"
        params = []

        if search:
            query += " WHERE nombre_categoria ILIKE %s OR descripcion ILIKE %s"
            term = f"%{search.strip()}%"
            params.extend([term, term])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_categoria: int) -> Optional[dict]:
        """Obtiene una categoría por su ID."""
        query = "SELECT id_categoria, nombre_categoria, descripcion FROM categoria WHERE id_categoria = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_categoria,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre_categoria: str, descripcion: Optional[str] = None) -> int:
        """Inserta una nueva categoría y retorna su ID generado."""
        query = """
            INSERT INTO categoria (nombre_categoria, descripcion)
            VALUES (%s, %s)
            RETURNING id_categoria
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_categoria.strip(), descripcion.strip() if descripcion else None))
                row = cur.fetchone()
                return row["id_categoria"]
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe una categoría con ese nombre.") from e

    @staticmethod
    def update(id_categoria: int, nombre_categoria: str, descripcion: Optional[str] = None) -> bool:
        """Actualiza los datos de una categoría existente."""
        query = """
            UPDATE categoria
            SET nombre_categoria = %s, descripcion = %s
            WHERE id_categoria = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_categoria.strip(), descripcion.strip() if descripcion else None, id_categoria))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Categoría con ID {id_categoria} no encontrada.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe una categoría con ese nombre.") from e

    @staticmethod
    def count_references(id_categoria: int) -> int:
        """Cuenta la cantidad de productos asociados a esta categoría."""
        query = "SELECT COUNT(*) AS total FROM producto WHERE id_categoria = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_categoria,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_categoria: int) -> bool:
        """Elimina una categoría si no tiene productos dependientes."""
        refs = CategoriaRepository.count_references(id_categoria)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} producto(s).",
                count=refs
            )

        query = "DELETE FROM categoria WHERE id_categoria = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_categoria,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Categoría con ID {id_categoria} no encontrada.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
