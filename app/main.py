import logging
from logging.handlers import RotatingFileHandler
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings, BASE_DIR
from app.database import init_db_pool, close_db_pool
from app.routers import abm, productos, stock, ventas, compras, devoluciones, dashboard, reportes

# Configuración del Logging
settings.log_path  # asegura creación del directorio logs/
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        RotatingFileHandler(settings.log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación: inicializa y libera recursos."""
    logger.info("Iniciando aplicación de Marroquinería...")
    try:
        init_db_pool()
    except Exception as e:
        logger.warning(
            "No se pudo conectar a la base de datos al iniciar (%s). "
            "Asegúrese de configurar el archivo .env correctamente.",
            e
        )
    yield
    logger.info("Apagando aplicación de Marroquinería...")
    close_db_pool()


app = FastAPI(
    title="Sistema de Gestión de Marroquinería",
    description="Aplicación local para gestión de marroquinería",
    version="1.0.0",
    lifespan=lifespan
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")


@app.middleware("http")
async def force_html_utf8(request: Request, call_next):
    """Asegura charset UTF-8 en respuestas HTML para que las tildes se vean bien."""
    response = await call_next(request)
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("text/html") and "charset=" not in content_type.lower():
        response.headers["content-type"] = "text/html; charset=utf-8"
    return response


# Incluir routers
app.include_router(dashboard.router)
app.include_router(abm.router)
app.include_router(productos.router)
app.include_router(stock.router)
app.include_router(ventas.router)
app.include_router(compras.router)
app.include_router(devoluciones.router)
app.include_router(reportes.router)


# Redirección de la raíz al Dashboard
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard")
