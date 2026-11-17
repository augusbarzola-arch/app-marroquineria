import logging
from logging.handlers import RotatingFileHandler
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings, BASE_DIR
from app.database import init_db_pool, close_db_pool
from app.services.scheduler import iniciar_scheduler, detener_scheduler
from app.routers import abm, productos, stock, ventas, compras, devoluciones, dashboard, reportes, ecommerce

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
    settings.upload_path  # asegura creación de app/static/uploads/
    try:
        init_db_pool()
        iniciar_scheduler()
    except Exception as e:
        logger.warning(
            "No se pudo conectar a la base de datos o iniciar scheduler (%s). "
            "Asegúrese de configurar el archivo .env correctamente.",
            e
        )
    yield
    logger.info("Apagando aplicación de Marroquinería...")
    detener_scheduler()
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
app.include_router(ecommerce.router)


# Redirección de la raíz a la Tienda Pública
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/tienda")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejo de errores para mostrar detalles técnicos en caso de fallo."""
    import traceback
    logger.exception("Error procesando solicitud en %s: %s", request.url.path, exc)
    from fastapi.responses import HTMLResponse
    tb = traceback.format_exc()
    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html lang="es">
        <head><meta charset="utf-8"><title>Error del Servidor</title></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f7fafc; padding: 40px 20px;">
            <div style="max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #e53e3e;">
                <h3 style="color: #9b2c2c; margin-top: 0;">Error interno en el servidor (500)</h3>
                <p><strong>Ruta:</strong> <code>{request.url.path}</code></p>
                <p><strong>Mensaje:</strong> <span style="color: #c53030; font-weight: 600;">{str(exc)}</span></p>
                <details style="margin-top: 20px;" open>
                    <summary style="cursor: pointer; color: #4a5568; font-weight: 500;">Detalle técnico (Traceback):</summary>
                    <pre style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 12px; margin-top: 10px; line-height: 1.4;">{tb}</pre>
                </details>
            </div>
        </body>
        </html>
        """,
        status_code=500
    )
