import os
from decimal import Decimal
from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Configuración general del sistema cargada desde variables de entorno."""

    # Conexión a PostgreSQL (local o nube como Supabase)
    DATABASE_URL: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "marroquineria"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_MIN_CONN: int = 1
    DB_MAX_CONN: int = 10

    # Servidor FastAPI / Uvicorn (soporte para Render/Railway)
    PORT: Optional[int] = None
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    BASE_URL: str = "http://127.0.0.1:8000"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Mercado Pago
    MP_ACCESS_TOKEN: str = "TEST-0000000000000000-000000-00000000000000000000000000000000-000000000"
    MP_WEBHOOK_SECRET: str = ""

    # Datos bancarios para transferencias
    BANK_ALIAS: str = "marroquineria.parana"
    BANK_CBU: str = "0000003100010000000000"
    BANK_TITULAR: str = "Marroquinería Paraná"
    BANK_BANCO: str = "Banco de Entre Ríos"

    # WhatsApp Oficial para recepción de comprobantes
    WHATSAPP_NUMERO: str = "5493435123456"

    # Envíos en Paraná y Alrededores (Moto Uber / Didi)
    ENVIO_GRATIS_MINIMO: Decimal = Decimal("30000.00")
    COSTO_ENVIO_PARANA: Decimal = Decimal("3000.00")
    COSTO_ENVIO_ALREDEDORES: Decimal = Decimal("4000.00")
    COSTO_ENVIO_CENTRO: Decimal = Decimal("3000.00")
    COSTO_ENVIO_NORTE: Decimal = Decimal("3000.00")
    COSTO_ENVIO_SUR: Decimal = Decimal("3000.00")

    # Notificaciones por Correo (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    NOTIFICATION_EMAIL: str = "dueno@marroquineria.com"

    # Almacenamiento local de archivos (comprobantes y fotos de productos)
    UPLOAD_FOLDER: str = "app/static/uploads"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def server_port(self) -> int:
        """Puerto para uvicorn (toma PORT de Render/Railway si está definido)."""
        return self.PORT or self.APP_PORT

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

    @property
    def upload_path(self) -> Path:
        """Ruta al directorio de uploads."""
        path = BASE_DIR / self.UPLOAD_FOLDER
        path.mkdir(parents=True, exist_ok=True)
        (path / "productos").mkdir(parents=True, exist_ok=True)
        (path / "comprobantes").mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
