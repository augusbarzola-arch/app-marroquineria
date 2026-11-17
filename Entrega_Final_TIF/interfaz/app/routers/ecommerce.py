import os
import shutil
import uuid
from typing import Optional
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, Query, status, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.config import settings
from app.templating import templates
from app.database import DatabaseError, RecordNotFoundError
from app.models.ecommerce import (
    CheckoutTransferenciaCreate,
    CheckoutMercadoPagoCreate
)
from app.repositories.ecommerce_repo import EcommerceRepository
from app.repositories.categoria_repo import CategoriaRepository
from app.services.ecommerce_service import EcommerceService

router = APIRouter(tags=["E-Commerce"])
PAGE_SIZE = 12


# ============================================================================
# VISTAS HTML - TIENDA PÚBLICA
# ============================================================================

@router.get("/tienda", response_class=HTMLResponse)
def tienda_catalogo(
    request: Request,
    page: int = Query(1, ge=1),
    categoria: Optional[int] = None,
    q: Optional[str] = None
):
    """Catálogo público de la tienda con precios web y 20% OFF en transferencia."""
    offset = (page - 1) * PAGE_SIZE
    total = EcommerceRepository.count_productos_tienda(id_categoria=categoria, search=q)
    productos_db = EcommerceRepository.get_productos_tienda(
        id_categoria=categoria,
        search=q,
        limit=PAGE_SIZE,
        offset=offset
    )

    # Inyectar estructura de precios calculada a cada producto
    productos = []
    for p in productos_db:
        precios = EcommerceService.calcular_precios(p["precio_base"])
        p["precios"] = precios
        productos.append(p)

    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total > 0 else 1
    categorias = CategoriaRepository.get_all()

    return templates.TemplateResponse(
        "tienda/catalogo.html",
        {
            "request": request,
            "productos": productos,
            "categorias": categorias,
            "selected_categoria": categoria,
            "search_query": q or "",
            "current_page": page,
            "total_pages": total_pages,
            "total_productos": total,
            "envio_gratis_minimo": settings.ENVIO_GRATIS_MINIMO
        }
    )


@router.get("/tienda/producto/{id_producto}", response_class=HTMLResponse)
def tienda_producto_detalle(request: Request, id_producto: int):
    """Ficha detallada del producto con galería de fotos, variantes y precios."""
    producto = EcommerceRepository.get_producto_detalle(id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    precios = EcommerceService.calcular_precios(producto["precio_base"])
    producto["precios"] = precios

    return templates.TemplateResponse(
        "tienda/producto.html",
        {
            "request": request,
            "producto": producto,
            "envio_gratis_minimo": settings.ENVIO_GRATIS_MINIMO
        }
    )


@router.get("/tienda/carrito", response_class=HTMLResponse)
def tienda_carrito(request: Request):
    """Página de Carrito y Checkout con selector de método de pago y zonas de entrega."""
    return templates.TemplateResponse(
        "tienda/carrito.html",
        {
            "request": request,
            "envio_gratis_minimo": settings.ENVIO_GRATIS_MINIMO,
            "costo_centro": settings.COSTO_ENVIO_CENTRO,
            "costo_norte": settings.COSTO_ENVIO_NORTE,
            "costo_sur": settings.COSTO_ENVIO_SUR,
            "bank_alias": settings.BANK_ALIAS,
            "bank_cbu": settings.BANK_CBU,
            "bank_titular": settings.BANK_TITULAR,
            "bank_banco": settings.BANK_BANCO
        }
    )


@router.get("/tienda/pedido/{codigo}", response_class=HTMLResponse)
def tienda_pedido_seguimiento(request: Request, codigo: str, status_param: Optional[str] = Query(None, alias="status")):
    """Página de estado del pedido, datos bancarios para transferencia y subida de comprobante."""
    pedido = EcommerceRepository.get_pedido_by_codigo(codigo)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    return templates.TemplateResponse(
        "tienda/pedido.html",
        {
            "request": request,
            "pedido": pedido,
            "status_param": status_param,
            "bank_alias": settings.BANK_ALIAS,
            "bank_cbu": settings.BANK_CBU,
            "bank_titular": settings.BANK_TITULAR,
            "bank_banco": settings.BANK_BANCO
        }
    )


# ============================================================================
# ENDPOINTS REST PÚBLICOS - E-COMMERCE
# ============================================================================

@router.post("/api/tienda/checkout/transferencia")
def api_checkout_transferencia(datos: CheckoutTransferenciaCreate):
    """Procesa el carrito con transferencia bancaria (20% OFF) y genera orden pendiente."""
    try:
        resultado = EcommerceService.checkout_transferencia(datos)
        return resultado
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/api/tienda/checkout/mercadopago")
def api_checkout_mercadopago(datos: CheckoutMercadoPagoCreate):
    """Genera preferencia de Mercado Pago Checkout Pro con Precio Lista Web."""
    try:
        resultado = EcommerceService.checkout_mercadopago(datos)
        return resultado
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/api/tienda/pedidos/{codigo}/comprobante")
async def api_subir_comprobante(codigo: str, comprobante: UploadFile = File(...)):
    """Permite al cliente subir la foto del comprobante de transferencia bancaria."""
    pedido = EcommerceRepository.get_pedido_by_codigo(codigo)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    ext = Path(comprobante.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".pdf", ".webp"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato no válido (solo JPG, PNG, WEBP o PDF)")

    upload_folder = settings.upload_path / "comprobantes"
    nuevo_nombre = f"comp_{codigo}_{uuid.uuid4().hex[:6]}{ext}"
    destino = upload_folder / nuevo_nombre

    with open(destino, "wb") as buffer:
        shutil.copyfileobj(comprobante.file, buffer)

    url_relativa = f"/static/uploads/comprobantes/{nuevo_nombre}"

    from app.database import get_db_cursor
    with get_db_cursor(commit=True) as cur:
        cur.execute("UPDATE pedido_web SET comprobante_url = %s WHERE id_pedido = %s", (url_relativa, pedido["id_pedido"]))

    return {"status": "ok", "url": url_relativa, "message": "Comprobante cargado correctamente."}


@router.post("/api/tienda/webhook/mercadopago")
async def api_webhook_mercadopago(request: Request):
    """Webhook oficial de Mercado Pago: valida firma, asegura idempotencia y descuenta stock."""
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    x_signature = request.headers.get("x-signature")
    res = EcommerceService.procesar_webhook_mercadopago(payload, x_signature)
    return JSONResponse(status_code=200, content=res)


# ============================================================================
# PANEL DE ADMINISTRACIÓN - E-COMMERCE
# ============================================================================

@router.get("/admin/ecommerce/pedidos", response_class=HTMLResponse)
def admin_pedidos_listado(
    request: Request,
    estado: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(1, ge=1)
):
    """Panel de administración para auditar pedidos web y aprobar transferencias."""
    limit = 20
    offset = (page - 1) * limit
    total = EcommerceRepository.count_pedidos(estado=estado, search=q)
    pedidos = EcommerceRepository.get_pedidos(estado=estado, search=q, limit=limit, offset=offset)
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return templates.TemplateResponse(
        "admin/pedidos.html",
        {
            "request": request,
            "pedidos": pedidos,
            "estado_filtro": estado or "",
            "search_query": q or "",
            "current_page": page,
            "total_pages": total_pages,
            "total_pedidos": total,
            "active_menu": "pedidos_web"
        }
    )


@router.get("/admin/ecommerce/pedidos/{id_pedido}", response_class=HTMLResponse)
def admin_pedido_detalle(request: Request, id_pedido: int):
    """Vista detallada del pedido con botón de aprobación y visualización del comprobante."""
    pedido = EcommerceRepository.get_pedido_by_id(id_pedido)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    return templates.TemplateResponse(
        "admin/pedido_detalle.html",
        {
            "request": request,
            "pedido": pedido,
            "active_menu": "pedidos_web"
        }
    )


@router.post("/admin/ecommerce/pedidos/{id_pedido}/aprobar")
def admin_aprobar_transferencia(id_pedido: int):
    """Acción de un clic para aprobar la transferencia bancaria y descontar el stock físico."""
    try:
        res = EcommerceService.aprobar_transferencia(id_pedido)
        return JSONResponse(content={"status": "ok", "message": "Pago aprobado con éxito. Stock descontado y venta registrada en POS.", "data": res})
    except (DatabaseError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/admin/ecommerce/pedidos/{id_pedido}/estado")
def admin_cambiar_estado_pedido(id_pedido: int, nuevo_estado: str = Form(...)):
    """Permite marcar pedido como 'ENVIADO' (despachado con Moto Uber) o 'CANCELADO'."""
    if nuevo_estado not in ["PENDIENTE_PAGO", "PAGADO", "ENVIADO", "CANCELADO"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado inválido")

    from app.database import get_db_cursor
    with get_db_cursor(commit=True) as cur:
        cur.execute("UPDATE pedido_web SET estado = %s WHERE id_pedido = %s", (nuevo_estado, id_pedido))

    return RedirectResponse(url=f"/admin/ecommerce/pedidos/{id_pedido}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/admin/ecommerce/productos/{id_producto}/imagenes")
async def admin_subir_imagen_producto(id_producto: int, imagen: UploadFile = File(...), es_portada: bool = Form(False)):
    """Sube una foto de producto a disco local y la asocia en la base de datos."""
    ext = Path(imagen.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de imagen no admitido")

    upload_folder = settings.upload_path / "productos"
    nuevo_nombre = f"prod_{id_producto}_{uuid.uuid4().hex[:8]}{ext}"
    destino = upload_folder / nuevo_nombre

    with open(destino, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    url_relativa = f"/static/uploads/productos/{nuevo_nombre}"
    id_img = EcommerceRepository.guardar_imagen(id_producto, url_relativa, es_portada=es_portada)

    return JSONResponse(content={"status": "ok", "id_imagen": id_img, "url": url_relativa})


@router.delete("/admin/ecommerce/imagenes/{id_imagen}")
def admin_eliminar_imagen(id_imagen: int):
    """Elimina una imagen asociada al producto."""
    ok = EcommerceRepository.eliminar_imagen(id_imagen)
    return JSONResponse(content={"status": "ok" if ok else "error"})
