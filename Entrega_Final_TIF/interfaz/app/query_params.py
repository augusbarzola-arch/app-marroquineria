from typing import Annotated, Optional
from pydantic import BeforeValidator


def _empty_to_none(value):
    """Convierte strings vacíos del query string (selects 'Todos') en None."""
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


OptionalIntQuery = Annotated[Optional[int], BeforeValidator(_empty_to_none)]
OptionalStrQuery = Annotated[Optional[str], BeforeValidator(_empty_to_none)]


def _to_bool(value):
    """Acepta checkbox HTML (true/on/1) y trata vacío como False."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("true", "1", "on", "yes", "si", "sí"):
            return True
        if v in ("false", "0", "off", "no"):
            return False
    return value


BoolQuery = Annotated[bool, BeforeValidator(_to_bool)]
