from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
)


class MaterialRepository:
    """Repositorio para la tabla 'material' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene materiales con filtro de búsqueda opcional y paginación."""
        query = "SELECT id_material, nombre_material FROM material"
        params = []

        if search:
            query += " WHERE nombre_material ILIKE %s"
            params.append(f"%{search.strip()}%")

        query += " ORDER BY id_material ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de materiales para paginación."""
        query = "SELECT COUNT(*) AS total FROM material"
        params = []

        if search:
            query += " WHERE nombre_material ILIKE %s"
            params.append(f"%{search.strip()}%")

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_material: int) -> Optional[dict]:
        """Obtiene un material por su ID."""
        query = "SELECT id_material, nombre_material FROM material WHERE id_material = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_material,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre_material: str) -> int:
        """Inserta un nuevo material y retorna su ID."""
        query = """
            INSERT INTO material (nombre_material)
            VALUES (%s)
            RETURNING id_material
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_material.strip(),))
                row = cur.fetchone()
                return row["id_material"]
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un material con ese nombre.") from e

    @staticmethod
    def update(id_material: int, nombre_material: str) -> bool:
        """Actualiza un material existente."""
        query = """
            UPDATE material
            SET nombre_material = %s
            WHERE id_material = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_material.strip(), id_material))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Material con ID {id_material} no encontrado.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un material con ese nombre.") from e

    @staticmethod
    def count_references(id_material: int) -> int:
        """Cuenta la cantidad de productos asociados a este material."""
        query = "SELECT COUNT(*) AS total FROM producto WHERE id_material = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_material,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_material: int) -> bool:
        """Elimina un material si no tiene productos dependientes."""
        refs = MaterialRepository.count_references(id_material)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} producto(s).",
                count=refs
            )

        query = "DELETE FROM material WHERE id_material = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_material,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Material con ID {id_material} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
