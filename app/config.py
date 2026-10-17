import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Configuración general del sistema cargada desde variables de entorno."""

    # Conexión a PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "marroquineria"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_MIN_CONN: int = 1
    DB_MAX_CONN: int = 10

    # Servidor FastAPI / Uvicorn
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def db_params(self) -> dict:
        """Retorna el diccionario con los parámetros de conexión para psycopg2."""
        return {
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "dbname": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "client_encoding": "UTF8",
        }

    @property
    def log_path(self) -> Path:
        """Retorna la ruta absoluta al archivo de logs y asegura su carpeta."""
        full_path = BASE_DIR / self.LOG_FILE
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return full_path


settings = Settings()
