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


class CompatibleJinja2Templates(Jinja2Templates):
    """
    Subclase compatible para Starlette/FastAPI:
    Unifica las llamadas antiguas y modernas de TemplateResponse:
    - TemplateResponse('template.html', {'request': request, ...})
    - TemplateResponse(request, 'template.html', {...})
    - TemplateResponse(request=request, name='template.html', context={...})
    Evita el error 'TypeError: unhashable type: dict' en versiones recientes de Starlette.
    """
    def TemplateResponse(self, *args, **kwargs):
        request = kwargs.get("request")
        name = kwargs.get("name")
        context = kwargs.get("context", {})

        if args:
            # Estilo antiguo: args[0] es el nombre del template
            if isinstance(args[0], str):
                name = args[0]
                if len(args) > 1 and isinstance(args[1], dict):
                    context = args[1]
                    if not request and "request" in context:
                        request = context["request"]
            # Estilo nuevo de Starlette: args[0] es la Request
            elif hasattr(args[0], "scope"):
                request = args[0]
                if len(args) > 1 and isinstance(args[1], str):
                    name = args[1]
                if len(args) > 2 and isinstance(args[2], dict):
                    context = args[2]

        if not name:
            name = kwargs.get("name")
        if not context:
            context = kwargs.get("context", {})
        if not request and isinstance(context, dict) and "request" in context:
            request = context["request"]

        # Invocar siempre con argumentos por clave explícitos
        return super().TemplateResponse(
            request=request,
            name=name,
            context=context,
            status_code=kwargs.get("status_code", 200),
            headers=kwargs.get("headers"),
            media_type=kwargs.get("media_type"),
            background=kwargs.get("background")
        )


templates = CompatibleJinja2Templates(env=_env)
