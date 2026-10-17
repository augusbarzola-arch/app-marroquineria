import logging
from contextlib import contextmanager
from typing import Generator, Optional
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from app.config import settings

logger = logging.getLogger("app.database")

# Instancia global del pool
_pool: Optional[pool.ThreadedConnectionPool] = None


class DatabaseError(Exception):
    """Excepción base para operaciones de base de datos."""
    pass


class RecordNotFoundError(DatabaseError):
    """Excepción cuando no se encuentra un registro requerido."""
    pass


class UniqueConstraintError(DatabaseError):
    """Excepción por duplicación en campo UNIQUE."""
    pass


class ForeignKeyConstraintError(DatabaseError):
    """Excepción cuando no se puede eliminar un registro por estar referenciado."""
    def __init__(self, message: str, count: int = 0):
        super().__init__(message)
        self.count = count


def init_db_pool() -> pool.ThreadedConnectionPool:
    """Inicializa el pool de conexiones seguras y multihilo a PostgreSQL."""
    global _pool
    if _pool is None or _pool.closed:
        try:
            logger.info("Inicializando ThreadedConnectionPool a PostgreSQL...")
            _pool = pool.ThreadedConnectionPool(
                minconn=settings.DB_MIN_CONN,
                maxconn=settings.DB_MAX_CONN,
                **settings.db_params
            )
            logger.info("Pool de conexiones iniciado correctamente.")
        except Exception as e:
            logger.error("Fallo al inicializar el pool de conexiones: %s", e)
            raise DatabaseError(f"No se pudo conectar a la base de datos: {e}") from e
    return _pool


def get_pool() -> pool.ThreadedConnectionPool:
    """Obtiene el pool existente o lo inicializa si aún no existe."""
    global _pool
    if _pool is None or _pool.closed:
        return init_db_pool()
    return _pool


def close_db_pool() -> None:
    """Cierra todas las conexiones activas del pool al apagar el servidor."""
    global _pool
    if _pool is not None and not _pool.closed:
        logger.info("Cerrando todas las conexiones del pool...")
        _pool.closeall()
        _pool = None
        logger.info("Pool de conexiones cerrado con éxito.")


@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """Context manager para obtener y devolver una conexión individual al pool."""
    p = get_pool()
    conn = p.getconn()
    try:
        if conn.encoding != "UTF8":
            conn.set_client_encoding("UTF8")
        yield conn
    finally:
        p.putconn(conn)


@contextmanager
def get_db_cursor(commit: bool = False) -> Generator[RealDictCursor, None, None]:
    """Context manager que proporciona un cursor tipo diccionario (RealDictCursor).
    Si commit=True, confirma automáticamente al terminar sin excepciones.
    Si ocurre una excepción, ejecuta rollback.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


@contextmanager
def get_db_transaction() -> Generator[psycopg2.extensions.connection, None, None]:
    """Context manager explícito para transacciones multi-tabla.
    Garantiza COMMIT al finalizar con éxito o ROLLBACK ante cualquier excepción.
    """
    with get_db_connection() as conn:
        try:
            conn.autocommit = False
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
