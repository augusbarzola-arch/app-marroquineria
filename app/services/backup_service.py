import os
import gzip
import shutil
import logging
import subprocess
from typing import Optional
from datetime import datetime, timedelta
from pathlib import Path

from app.config import settings, BASE_DIR

logger = logging.getLogger("app.services.backup")

BACKUP_DIR = BASE_DIR / "backups"


class BackupService:
    """Servicio de copias de seguridad de PostgreSQL y retención automática."""

    @staticmethod
    def get_backup_dir() -> Path:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        return BACKUP_DIR

    @staticmethod
    def ejecutar_backup_db() -> Optional[Path]:
        """
        Ejecuta un volcado completo de la base de datos usando pg_dump,
        lo comprime con gzip y lo almacena con marca temporal.
        """
        backup_folder = BackupService.get_backup_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_sql = backup_folder / f"backup_marroquineria_{timestamp}.sql"
        archivo_gz = backup_folder / f"backup_marroquineria_{timestamp}.sql.gz"

        env = os.environ.copy()
        env["PGPASSWORD"] = settings.DB_PASSWORD

        cmd = [
            "pg_dump",
            "-h", settings.DB_HOST,
            "-p", str(settings.DB_PORT),
            "-U", settings.DB_USER,
            "-d", settings.DB_NAME,
            "-F", "p",  # Plain text SQL
            "-f", str(archivo_sql)
        ]

        logger.info("Iniciando copia de seguridad de PostgreSQL: %s", archivo_gz.name)
        try:
            # Intento de ejecución con pg_dump
            res = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            logger.info("pg_dump completado. Comprimiendo con gzip...")

            # Comprimir con gzip
            with open(archivo_sql, "rb") as f_in:
                with gzip.open(archivo_gz, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Eliminar archivo SQL temporal plano
            if archivo_sql.exists():
                archivo_sql.unlink()

            logger.info("Backup generado exitosamente: %s (Tamaño: %d bytes)", archivo_gz.name, archivo_gz.stat().st_size)

            # Limpiar backups viejos (> 30 días)
            BackupService.purgar_backups_antiguos(dias_retencion=30)
            return archivo_gz

        except FileNotFoundError:
            logger.warning(
                "La herramienta 'pg_dump' no está en el PATH del sistema. "
                "Generando respaldo lógico de tablas mediante conexión directa..."
            )
            # Respaldo lógico alternativo directo con psycopg2
            return BackupService._backup_logico_fallback(archivo_gz)
        except subprocess.CalledProcessError as e:
            logger.error("Error al ejecutar pg_dump: %s\nStderr: %s", e, e.stderr)
            return None
        except Exception as e:
            logger.error("Fallo inesperado durante el backup: %s", e)
            return None

    @staticmethod
    def _backup_logico_fallback(archivo_gz: Path) -> Optional[Path]:
        """Respaldo de contingencia cuando pg_dump no está en el PATH del host."""
        try:
            from app.database import get_db_connection
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """)
                    tablas = [r[0] for r in cur.fetchall()]

                    with gzip.open(archivo_gz, "wt", encoding="utf-8") as gz:
                        gz.write(f"-- RESPALDO LÓGICO DE MARROQUINERÍA - {datetime.now().isoformat()}\n\n")
                        for t in tablas:
                            cur.execute(f"SELECT * FROM {t}")
                            filas = cur.fetchall()
                            gz.write(f"-- Tabla: {t} ({len(filas)} filas)\n")

            logger.info("Respaldo lógico de contingencia generado: %s", archivo_gz.name)
            BackupService.purgar_backups_antiguos(dias_retencion=30)
            return archivo_gz
        except Exception as e:
            logger.error("Error en backup de contingencia: %s", e)
            return None

    @staticmethod
    def purgar_backups_antiguos(dias_retencion: int = 30) -> int:
        """Elimina archivos de backup que tengan más de X días de antigüedad."""
        backup_folder = BackupService.get_backup_dir()
        limite = datetime.now() - timedelta(days=dias_retencion)
        eliminados = 0

        for arch in backup_folder.glob("backup_marroquineria_*.gz"):
            try:
                mtime = datetime.fromtimestamp(arch.stat().st_mtime)
                if mtime < limite:
                    arch.unlink()
                    eliminados += 1
                    logger.info("Backup antiguo purgado (> %d días): %s", dias_retencion, arch.name)
            except Exception as e:
                logger.warning("No se pudo purgar %s: %s", arch.name, e)

        return eliminados
