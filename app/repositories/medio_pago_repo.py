from decimal import Decimal
from typing import List, Optional, Union
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, CheckViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
    DatabaseError,
)


class MedioPagoRepository:
    """Repositorio para la tabla 'medio_pago' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Obtiene medios de pago con filtro opcional y paginación."""
        query = "SELECT id_medio_pago, nombre_medio, porcentaje_descuento_recargo FROM medio_pago"
        params = []

        if search:
            query += " WHERE nombre_medio ILIKE %s"
            params.append(f"%{search.strip()}%")

        query += " ORDER BY id_medio_pago ASC"

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(search: Optional[str] = None) -> int:
        """Cuenta el total de medios de pago para paginación."""
        query = "SELECT COUNT(*) AS total FROM medio_pago"
        params = []

        if search:
            query += " WHERE nombre_medio ILIKE %s"
            params.append(f"%{search.strip()}%")

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_medio_pago: int) -> Optional[dict]:
        """Obtiene un medio de pago por su ID."""
        query = "SELECT id_medio_pago, nombre_medio, porcentaje_descuento_recargo FROM medio_pago WHERE id_medio_pago = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_medio_pago,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre_medio: str, porcentaje_descuento_recargo: Union[float, Decimal] = 0.0) -> int:
        """Inserta un nuevo medio de pago validando el rango de porcentaje (-100 a 100)."""
        pct = float(porcentaje_descuento_recargo)
        if pct < -100.0 or pct > 100.0:
            raise DatabaseError("El porcentaje debe estar comprendido entre -100 y 100.")

        query = """
            INSERT INTO medio_pago (nombre_medio, porcentaje_descuento_recargo)
            VALUES (%s, %s)
            RETURNING id_medio_pago
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_medio.strip(), pct))
                row = cur.fetchone()
                return row["id_medio_pago"]
        except CheckViolation as e:
            raise DatabaseError("El porcentaje de descuento/recargo debe estar entre -100 y 100.") from e
        except UniqueViolation as e:
            raise UniqueConstraintError("Ya existe un medio de pago con ese nombre.") from e

    @staticmethod
    def update(
        id_medio_pago: int,
        nombre_medio: str,
        porcentaje_descuento_recargo: Union[float, Decimal]
    ) -> bool:
        """Actualiza un medio de pago existente."""
        pct = float(porcentaje_descuento_recargo)
        if pct < -100.0 or pct > 100.0:
            raise DatabaseError("El porcentaje debe estar comprendido entre -100 y 100.")

        query = """
            UPDATE medio_pago
            SET nombre_medio = %s, porcentaje_descuento_recargo = %s
            WHERE id_medio_pago = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (nombre_medio.strip(), pct, id_medio_pago))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Medio de pago con ID {id_medio_pago} no encontrado.")
                return True
        except CheckViolation as e:
            raise DatabaseError("El porcentaje de descuento/recargo debe estar entre -100 y 100.") from e
        except UniqueViolation as e:
            raise UniqueConstraintError("Ya existe un medio de pago con ese nombre.") from e

    @staticmethod
    def count_references(id_medio_pago: int) -> int:
        """Cuenta la cantidad de ventas asociadas a este medio de pago."""
        query = "SELECT COUNT(*) AS total FROM venta WHERE id_medio_pago = %s"
        with get_db_cursor() as cur:
            cur.execute(query, (id_medio_pago,))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_medio_pago: int) -> bool:
        """Elimina un medio de pago si no tiene ventas asociadas."""
        refs = MedioPagoRepository.count_references(id_medio_pago)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque está siendo usado por {refs} venta(s).",
                count=refs
            )

        query = "DELETE FROM medio_pago WHERE id_medio_pago = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_medio_pago,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Medio de pago con ID {id_medio_pago} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
