"""
tunnel_runner.py - Supervisor y auto-reinicio de Cloudflare Tunnel
Expone la aplicación FastAPI local a una URL pública y segura con HTTPS.
Si el túnel se desconecta o falla, lo reinicia automáticamente.
"""

import sys
import time
import shutil
import logging
import subprocess
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLOUDFLARE-TUNNEL] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/tunnel.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("tunnel_runner")

LOCAL_SERVER_URL = "http://127.0.0.1:8000"


def check_cloudflared_installed() -> bool:
    """Verifica si cloudflared está en el PATH del sistema."""
    return shutil.which("cloudflared") is not None


def run_tunnel_with_autorestart():
    """Ejecuta el túnel y lo vigila de forma continua, reiniciándolo si se cae."""
    if not check_cloudflared_installed():
        logger.error(
            "No se encontró el ejecutable 'cloudflared' en el PATH del sistema.\n"
            "Para instalarlo en Windows ejecutá:\n"
            "   winget install --id Cloudflare.cloudflared\n"
            "O descargá el binario desde:\n"
            "   https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe\n"
            "y colócalo en esta carpeta como 'cloudflared.exe'."
        )
        return

    cmd = ["cloudflared", "tunnel", "--url", LOCAL_SERVER_URL]
    logger.info("Iniciando túnel Cloudflare hacia %s...", LOCAL_SERVER_URL)

    reintentos = 0
    while True:
        try:
            inicio = datetime.now()
            logger.info("Lanzando proceso: %s", " ".join(cmd))
            proceso = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            for linea in proceso.stdout:
                linea_limpia = linea.strip()
                if "trycloudflare.com" in linea_limpia:
                    logger.info("==================================================")
                    logger.info("🟢 URL PÚBLICA DEL TÚNEL DETECTADA:")
                    logger.info("👉 %s", linea_limpia)
                    logger.info("==================================================")
                else:
                    logger.info(linea_limpia)

            proceso.wait()
            duracion = (datetime.now() - inicio).total_seconds()
            logger.warning("El proceso cloudflared terminó con código %s tras %.1f segundos.", proceso.returncode, duracion)

        except Exception as e:
            logger.error("Excepción inesperada al ejecutar cloudflared: %s", e)

        # Si duró más de 60 segundos, reiniciamos el contador de reintentos
        if duracion > 60:
            reintentos = 0
        else:
            reintentos += 1

        pausa = min(30, 2 ** reintentos)
        logger.info("Reiniciando túnel en %d segundos... (Reintento #%d)", pausa, reintentos)
        time.sleep(pausa)


if __name__ == "__main__":
    run_tunnel_with_autorestart()
