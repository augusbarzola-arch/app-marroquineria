import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.services.backup_service import BackupService
from app.services.ecommerce_service import EcommerceService

logger = logging.getLogger("app.services.scheduler")

_scheduler = None


def iniciar_scheduler():
    """Inicializa y arranca las tareas programadas en segundo plano."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        return _scheduler

    logger.info("Iniciando APScheduler para tareas en segundo plano...")
    _scheduler = BackgroundScheduler(daemon=True)

    # 1. Backup diario a las 02:00 AM
    _scheduler.add_job(
        func=BackupService.ejecutar_backup_db,
        trigger=CronTrigger(hour=2, minute=0),
        id="backup_diario_postgres",
        name="Backup diario de PostgreSQL a las 2 AM",
        replace_existing=True
    )

    # 2. Expiración de pedidos por transferencia pendientes > 24hs cada 30 minutos
    _scheduler.add_job(
        func=EcommerceService.expirar_pedidos_vencidos,
        trigger=IntervalTrigger(minutes=30),
        id="expiracion_pedidos_transferencia",
        name="Expirar pedidos por transferencia vencidos (24h)",
        replace_existing=True
    )

    _scheduler.start()
    logger.info("APScheduler iniciado con éxito (Backup 2 AM y Expiración 24hs).")
    return _scheduler


def detener_scheduler():
    """Detiene limpiamente el planificador al apagar el servidor."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        logger.info("Deteniendo APScheduler...")
        _scheduler.shutdown(wait=False)
        _scheduler = None
