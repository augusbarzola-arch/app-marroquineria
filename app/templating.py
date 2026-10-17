from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR

# Carga explícita en UTF-8 para evitar mojibake de tildes en Windows.
_env = Environment(
    loader=FileSystemLoader(
        str(BASE_DIR / "app" / "templates"),
        encoding="utf-8",
    ),
    autoescape=select_autoescape(["html", "xml"]),
)

templates = Jinja2Templates(env=_env)
