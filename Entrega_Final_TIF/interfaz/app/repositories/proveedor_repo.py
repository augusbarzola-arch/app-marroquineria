from typing import List, Optional
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
)


class ProveedorRepository:
    """Repositorio para la tabla 'proveedor' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene proveedores con filtro de búsqueda opcional y paginación."""
        query = "SELECT id_proveedor, cuit, razon_social, telefono, email FROM proveedor"
        params = []

        if search:
            query += " WHERE razon_social ILIKE %s OR cuit ILIKE %s OR email ILIKE %s"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        query += " ORDER BY id_proveedor ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de proveedores para paginación."""
        query = "SELECT COUNT(*) AS total FROM proveedor"
        params = []

        if search:
            query += " WHERE razon_social ILIKE %s OR cuit ILIKE %s OR email ILIKE %s"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_proveedor: int) -> Optional[dict]:
        """Obtiene un proveedor por su ID."""
        query = "SELECT id_proveedor, cuit, razon_social, telefono, email FROM proveedor WHERE id_proveedor = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_proveedor,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_cuit(cuit: str) -> Optional[dict]:
        """Obtiene un proveedor por su CUIT."""
        query = "SELECT id_proveedor, cuit, razon_social, telefono, email FROM proveedor WHERE cuit = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (cuit.strip(),))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(
        cuit: str,
        razon_social: str,
        telefono: Optional[str] = None,
        email: Optional[str] = None
    ) -> int:
        """Inserta un nuevo proveedor y retorna su ID."""
        query = """
            INSERT INTO proveedor (cuit, razon_social, telefono, email)
            VALUES (%s, %s, %s, %s)
            RETURNING id_proveedor
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (
                    cuit.strip(),
                    razon_social.strip(),
                    telefono.strip() if telefono else None,
                    email.strip() if email else None
                ))
                row = cur.fetchone()
                return row["id_proveedor"]
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un proveedor con el CUIT '{cuit.strip()}'.") from e

    @staticmethod
    def update(
        id_proveedor: int,
        cuit: str,
        razon_social: str,
        telefono: Optional[str] = None,
        email: Optional[str] = None
    ) -> bool:
        """Actualiza un proveedor existente."""
        query = """
            UPDATE proveedor
            SET cuit = %s, razon_social = %s, telefono = %s, email = %s
            WHERE id_proveedor = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (
                    cuit.strip(),
                    razon_social.strip(),
                    telefono.strip() if telefono else None,
                    email.strip() if email else None,
                    id_proveedor
                ))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Proveedor con ID {id_proveedor} no encontrado.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"Ya existe un proveedor con el CUIT '{cuit.strip()}'.") from e

    @staticmethod
    def count_references(id_proveedor: int) -> int:
        """Cuenta la cantidad de compras asociadas a este proveedor."""
        query = "SELECT COUNT(*) AS total FROM compra WHERE id_proveedor = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_proveedor,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_proveedor: int) -> bool:
        """Elimina un proveedor si no tiene compras registradas."""
        refs = ProveedorRepository.count_references(id_proveedor)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} compra(s).",
                count=refs
            )

        query = "DELETE FROM proveedor WHERE id_proveedor = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_proveedor,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Proveedor con ID {id_proveedor} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
