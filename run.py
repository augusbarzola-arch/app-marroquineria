import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Iniciando servidor en http://{settings.APP_HOST}:{settings.server_port} ...")
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.server_port,
        reload=settings.DEBUG
    )
