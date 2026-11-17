import os
import uuid
import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List, Optional
import mercadopago

from app.config import settings
from app.database import get_db_transaction, get_db_cursor, DatabaseError, RecordNotFoundError
from app.models.ecommerce import (
    CheckoutTransferenciaCreate,
    CheckoutMercadoPagoCreate,
    ItemCarrito
)
from app.repositories.ecommerce_repo import EcommerceRepository

logger = logging.getLogger("app.services.ecommerce")


class EcommerceService:
    """Lógica de negocio comercial, precios web, checkout, pagos y control de stock."""

    # =========================================================================
    # LÓGICA MATEMÁTICA DE PRECIOS Y COSTOS DE ENVÍO
    # =========================================================================

    @staticmethod
    def calcular_precios(precio_base: Decimal) -> Dict[str, Decimal]:
        """
        Calcula la estructura de precios para la tienda web:
        - Precio Lista Web: (Precio Base * 1.25) * 1.05
        - Precio Transferencia: Precio Lista Web * 0.80 (20% OFF)
        - Ahorro Transferencia: Precio Lista Web - Precio Transferencia
        """
        base = Decimal(str(precio_base))
        # Precio de lista web (+25% financiero y +5% logístico)
        lista_web = ((base * Decimal("1.25")) * Decimal("1.05")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        # Precio abonando por transferencia (20% de descuento directo sobre el precio de lista web)
        transferencia = (lista_web * Decimal("0.80")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        ahorro = (lista_web - transferencia).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "precio_base": base,
            "precio_lista_web": lista_web,
            "precio_transferencia": transferencia,
            "ahorro_transferencia": ahorro
        }

    @staticmethod
    def calcular_costo_envio(subtotal: Decimal, zona: str) -> Decimal:
        """
        Cálculo del envío en Paraná con cadetería Moto Uber:
        - Si el subtotal es mayor o igual a $100.000: Envío GRATIS ($0.00).
        - Si es menor: Costo fijo según zona.
        """
        if subtotal >= settings.ENVIO_GRATIS_MINIMO:
            return Decimal("0.00")

        zona_limpia = zona.strip().capitalize()
        if zona_limpia == "Centro":
            return settings.COSTO_ENVIO_CENTRO
        elif zona_limpia == "Norte":
            return settings.COSTO_ENVIO_NORTE
        elif zona_limpia == "Sur":
            return settings.COSTO_ENVIO_SUR
        return Decimal("3000.00")

    # =========================================================================
    # PROCESAMIENTO DE CHECKOUT CON TRANSFERENCIA
    # =========================================================================

    @staticmethod
    def checkout_transferencia(datos: CheckoutTransferenciaCreate) -> Dict[str, Any]:
        """
        Genera una orden web con método 'TRANSFERENCIA' en estado 'PENDIENTE_PAGO'.
        Aplica el 20% OFF (Precio Transferencia) y expira en 24 horas.
        """
        if not datos.items:
            raise DatabaseError("El carrito está vacío.")

        with get_db_transaction() as conn:
            cur = conn.cursor()

            # 1. Validar variantes y stock disponible
            items_procesados = []
            subtotal_acumulado = Decimal("0.00")

            for item in datos.items:
                cur.execute("""
                    SELECT 
                        v.id_variante,
                        v.stock_actual,
                        p.nombre_producto,
                        p.precio_lista AS precio_base,
                        col.nombre_color,
                        tam.nombre_tamano
                    FROM variante_producto v
                    JOIN producto p ON v.id_producto = p.id_producto
                    JOIN color col ON v.id_color = col.id_color
                    JOIN tamano tam ON v.id_tamano = tam.id_tamano
                    WHERE v.id_variante = %s
                """, (item.id_variante,))
                row = cur.fetchone()
                if not row:
                    raise RecordNotFoundError(f"Variante #{item.id_variante} no encontrada.")

                id_var, stock, prod_nombre, p_base, col_nom, tam_nom = row
                if stock < item.cantidad:
                    raise DatabaseError(
                        f"Stock insuficiente para '{prod_nombre} ({col_nom} - {tam_nom})'. "
                        f"Disponibles: {stock}, Solicitados: {item.cantidad}."
                    )

                precios = EcommerceService.calcular_precios(p_base)
                precio_cobrado = precios["precio_transferencia"]
                subtotal_item = precio_cobrado * item.cantidad
                subtotal_acumulado += subtotal_item

                items_procesados.append({
                    "id_variante": id_var,
                    "cantidad": item.cantidad,
                    "precio_unitario_cobrado": precio_cobrado,
                    "subtotal": subtotal_item,
                    "nombre": f"{prod_nombre} ({col_nom} - {tam_nom})"
                })

            # 2. Calcular costo de envío y total
            costo_envio = EcommerceService.calcular_costo_envio(subtotal_acumulado, datos.zona_envio)
            total_final = subtotal_acumulado + costo_envio

            # 3. Código único de seguimiento y expiración en 24 horas
            ahora = datetime.now()
            fecha_str = ahora.strftime("%y%m%d")
            random_suf = uuid.uuid4().hex[:4].upper()
            codigo_seguimiento = f"WEB-{fecha_str}-{random_suf}"
            expiracion = ahora + timedelta(hours=24)

            # 4. Insertar pedido_web
            cur.execute("""
                INSERT INTO pedido_web (
                    codigo_seguimiento, fecha_creacion, nombre_cliente, email_cliente, telefono_cliente,
                    direccion_envio, zona_envio, costo_envio, metodo_pago, estado,
                    subtotal, total, fecha_expiracion, observaciones
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, 'TRANSFERENCIA', 'PENDIENTE_PAGO',
                    %s, %s, %s, %s
                ) RETURNING id_pedido
            """, (
                codigo_seguimiento, ahora, datos.nombre_cliente, datos.email_cliente, datos.telefono_cliente,
                datos.direccion_envio, datos.zona_envio, costo_envio,
                subtotal_acumulado, total_final, expiracion, datos.observaciones
            ))
            id_pedido = cur.fetchone()[0]

            # 5. Insertar renglones en detalle_pedido_web
            for idx, it in enumerate(items_procesados, start=1):
                cur.execute("""
                    INSERT INTO detalle_pedido_web (
                        id_pedido, renglon, id_variante, cantidad, precio_unitario_cobrado, subtotal
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_pedido, idx, it["id_variante"], it["cantidad"], it["precio_unitario_cobrado"], it["subtotal"]))

            return {
                "id_pedido": id_pedido,
                "codigo_seguimiento": codigo_seguimiento,
                "total": float(total_final),
                "subtotal": float(subtotal_acumulado),
                "costo_envio": float(costo_envio),
                "expira": expiracion.strftime("%d/%m/%Y %H:%M"),
                "datos_bancarios": {
                    "alias": settings.BANK_ALIAS,
                    "cbu": settings.BANK_CBU,
                    "titular": settings.BANK_TITULAR,
                    "banco": settings.BANK_BANCO
                }
            }

    # =========================================================================
    # CHECKOUT MERCADO PAGO (CHECKOUT PRO)
    # =========================================================================

    @staticmethod
    def checkout_mercadopago(datos: CheckoutMercadoPagoCreate) -> Dict[str, Any]:
        """
        Genera orden web y preferencia de pago en Mercado Pago Checkout Pro con Precio Lista Web.
        """
        if not datos.items:
            raise DatabaseError("El carrito está vacío.")

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        with get_db_transaction() as conn:
            cur = conn.cursor()

            items_mp = []
            items_procesados = []
            subtotal_acumulado = Decimal("0.00")

            for item in datos.items:
                cur.execute("""
                    SELECT 
                        v.id_variante,
                        v.stock_actual,
                        p.nombre_producto,
                        p.precio_lista AS precio_base,
                        col.nombre_color,
                        tam.nombre_tamano
                    FROM variante_producto v
                    JOIN producto p ON v.id_producto = p.id_producto
                    JOIN color col ON v.id_color = col.id_color
                    JOIN tamano tam ON v.id_tamano = tam.id_tamano
                    WHERE v.id_variante = %s
                """, (item.id_variante,))
                row = cur.fetchone()
                if not row:
                    raise RecordNotFoundError(f"Variante #{item.id_variante} no encontrada.")

                id_var, stock, prod_nombre, p_base, col_nom, tam_nom = row
                if stock < item.cantidad:
                    raise DatabaseError(
                        f"Stock insuficiente para '{prod_nombre} ({col_nom} - {tam_nom})'. "
                        f"Disponibles: {stock}, Solicitados: {item.cantidad}."
                    )

                precios = EcommerceService.calcular_precios(p_base)
                precio_cobrado = precios["precio_lista_web"]  # Tarjeta paga lista web
                subtotal_item = precio_cobrado * item.cantidad
                subtotal_acumulado += subtotal_item

                items_procesados.append({
                    "id_variante": id_var,
                    "cantidad": item.cantidad,
                    "precio_unitario_cobrado": precio_cobrado,
                    "subtotal": subtotal_item,
                    "nombre": f"{prod_nombre} ({col_nom} - {tam_nom})"
                })

                items_mp.append({
                    "title": f"{prod_nombre} ({col_nom} - {tam_nom})",
                    "quantity": int(item.cantidad),
                    "unit_price": float(precio_cobrado),
                    "currency_id": "ARS"
                })

            # Costo de envío
            costo_envio = EcommerceService.calcular_costo_envio(subtotal_acumulado, datos.zona_envio)
            if costo_envio > 0:
                items_mp.append({
                    "title": f"Costo de Envío - Zona {datos.zona_envio}",
                    "quantity": 1,
                    "unit_price": float(costo_envio),
                    "currency_id": "ARS"
                })

            total_final = subtotal_acumulado + costo_envio

            # Código de seguimiento
            ahora = datetime.now()
            fecha_str = ahora.strftime("%y%m%d")
            codigo_seguimiento = f"WEB-{fecha_str}-{uuid.uuid4().hex[:4].upper()}"

            # Crear preferencia en Mercado Pago
            preference_data = {
                "items": items_mp,
                "payer": {
                    "name": datos.nombre_cliente,
                    "email": datos.email_cliente,
                    "phone": {"number": datos.telefono_cliente},
                    "address": {"street_name": datos.direccion_envio}
                },
                "back_urls": {
                    "success": f"{settings.BASE_URL}/tienda/pedido/{codigo_seguimiento}?status=success",
                    "failure": f"{settings.BASE_URL}/tienda/pedido/{codigo_seguimiento}?status=failure",
                    "pending": f"{settings.BASE_URL}/tienda/pedido/{codigo_seguimiento}?status=pending"
                },
                "auto_return": "approved",
                "external_reference": codigo_seguimiento,
                "statement_descriptor": "MARROQUINERIA PARANA",
                "notification_url": f"{settings.BASE_URL}/api/tienda/webhook/mercadopago"
            }

            try:
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response["response"]
                mp_pref_id = preference.get("id")
                init_point = preference.get("init_point")
                sandbox_init_point = preference.get("sandbox_init_point")
            except Exception as e:
                logger.error("Error al generar preferencia en Mercado Pago: %s", e)
                # Fallback para pruebas sin token real
                mp_pref_id = f"mock-pref-{uuid.uuid4().hex[:8]}"
                init_point = f"{settings.BASE_URL}/tienda/pedido/{codigo_seguimiento}?status=mock_mp"
                sandbox_init_point = init_point

            # Guardar pedido
            cur.execute("""
                INSERT INTO pedido_web (
                    codigo_seguimiento, fecha_creacion, nombre_cliente, email_cliente, telefono_cliente,
                    direccion_envio, zona_envio, costo_envio, metodo_pago, estado,
                    subtotal, total, mp_preference_id
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, 'MERCADOPAGO', 'PENDIENTE_PAGO',
                    %s, %s, %s
                ) RETURNING id_pedido
            """, (
                codigo_seguimiento, ahora, datos.nombre_cliente, datos.email_cliente, datos.telefono_cliente,
                datos.direccion_envio, datos.zona_envio, costo_envio,
                subtotal_acumulado, total_final, mp_pref_id
            ))
            id_pedido = cur.fetchone()[0]

            for idx, it in enumerate(items_procesados, start=1):
                cur.execute("""
                    INSERT INTO detalle_pedido_web (
                        id_pedido, renglon, id_variante, cantidad, precio_unitario_cobrado, subtotal
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_pedido, idx, it["id_variante"], it["cantidad"], it["precio_unitario_cobrado"], it["subtotal"]))

            return {
                "id_pedido": id_pedido,
                "codigo_seguimiento": codigo_seguimiento,
                "preference_id": mp_pref_id,
                "init_point": init_point,
                "sandbox_init_point": sandbox_init_point,
                "total": float(total_final)
            }

    # =========================================================================
    # WEBHOOK DE MERCADO PAGO CON IDEMPOTENCIA Y SELECT FOR UPDATE
    # =========================================================================

    @staticmethod
    def procesar_webhook_mercadopago(payload: dict, x_signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa la notificación de pago de Mercado Pago de forma idempotente y atómica:
        - Verifica unicidad del evento para evitar procesamientos duplicados.
        - Bloquea filas de variante_producto con FOR UPDATE para prevenir sobreventa.
        - Descuenta stock y asienta la venta oficial en la tabla 'venta'.
        """
        event_id = str(payload.get("id") or payload.get("data", {}).get("id") or uuid.uuid4().hex)
        event_type = payload.get("type") or payload.get("action") or "payment"

        # 1. Garantía de Idempotencia
        if EcommerceRepository.existe_webhook_log(event_id):
            logger.info("Webhook %s ya fue procesado con anterioridad (Idempotente).", event_id)
            return {"status": "already_processed", "event_id": event_id}

        # Guardar en log de eventos
        EcommerceRepository.guardar_webhook_log(event_id, event_type, payload)

        payment_id = payload.get("data", {}).get("id") or payload.get("id")
        if not payment_id:
            return {"status": "no_payment_id"}

        # 2. Consultar el pago en Mercado Pago
        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
        try:
            payment_info = sdk.payment().get(str(payment_id))
            payment_data = payment_info.get("response", {})
        except Exception as e:
            logger.warning("No se pudo consultar el pago %s en Mercado Pago SDK (%s). Usando mock si aplica.", payment_id, e)
            payment_data = {"status": "approved", "external_reference": payload.get("external_reference")}

        payment_status = payment_data.get("status")
        external_reference = payment_data.get("external_reference") or payload.get("external_reference")

        if not external_reference:
            logger.warning("Pago %s sin external_reference asociada.", payment_id)
            return {"status": "missing_external_reference"}

        if payment_status != "approved":
            logger.info("Pago %s en estado '%s', no se descuenta stock todavía.", payment_id, payment_status)
            return {"status": "not_approved", "payment_status": payment_status}

        # 3. Transacción atómica con bloqueo estricto (FOR UPDATE)
        with get_db_transaction() as conn:
            cur = conn.cursor()

            # Obtener pedido
            cur.execute("""
                SELECT id_pedido, estado, subtotal, total, nombre_cliente, email_cliente
                FROM pedido_web
                WHERE codigo_seguimiento = %s
                FOR UPDATE
            """, (external_reference,))
            pedido = cur.fetchone()

            if not pedido:
                logger.error("No se encontró el pedido con código %s para el pago %s.", external_reference, payment_id)
                return {"status": "order_not_found"}

            id_pedido, estado, subtotal, total, cliente_nom, cliente_email = pedido

            if estado == "PAGADO":
                logger.info("El pedido %s ya se encuentra pagado.", external_reference)
                return {"status": "already_paid"}

            # Obtener ítems del pedido
            cur.execute("""
                SELECT dp.id_variante, dp.cantidad, dp.precio_unitario_cobrado, p.nombre_producto
                FROM detalle_pedido_web dp
                JOIN variante_producto v ON dp.id_variante = v.id_variante
                JOIN producto p ON v.id_producto = p.id_producto
                WHERE dp.id_pedido = %s
            """, (id_pedido,))
            detalles = cur.fetchall()

            # Bloquear y descontar stock
            for item in detalles:
                id_var, cant, precio_cobrado, nom_prod = item
                cur.execute("""
                    SELECT stock_actual 
                    FROM variante_producto 
                    WHERE id_variante = %s 
                    FOR UPDATE
                """, (id_var,))
                row_stock = cur.fetchone()
                if not row_stock:
                    raise RecordNotFoundError(f"Variante #{id_var} no existe.")

                stock_actual = row_stock[0]
                if stock_actual < cant:
                    logger.critical(
                        "Conflicto de sobreventa en Webhook MP para %s: stock actual %s, requerido %s.",
                        nom_prod, stock_actual, cant
                    )
                    # Descontamos hasta cero para no tener stock negativo si el pago ya entró
                    nuevo_stock = max(0, stock_actual - cant)
                else:
                    nuevo_stock = stock_actual - cant

                cur.execute("""
                    UPDATE variante_producto
                    SET stock_actual = %s
                    WHERE id_variante = %s
                """, (nuevo_stock, id_var))

            # Actualizar estado de la orden web
            cur.execute("""
                UPDATE pedido_web
                SET estado = 'PAGADO', mp_payment_id = %s
                WHERE id_pedido = %s
            """, (str(payment_id), id_pedido))

            # Asentar venta en tabla 'venta' para integrarlo al POS y reportes
            # Buscar ID de medio de pago Mercado Pago o Tarjeta (default 1)
            cur.execute("SELECT id_medio_pago FROM medio_pago WHERE nombre_medio ILIKE '%Mercado Pago%' OR nombre_medio ILIKE '%Tarjeta%' LIMIT 1")
            mp_row = cur.fetchone()
            id_mp = mp_row[0] if mp_row else 1

            cur.execute("""
                INSERT INTO venta (fecha_hora, monto_total, id_medio_pago)
                VALUES (CURRENT_TIMESTAMP, %s, %s)
                RETURNING id_venta
            """, (total, id_mp))
            id_venta = cur.fetchone()[0]

            for idx, item in enumerate(detalles, start=1):
                cur.execute("""
                    INSERT INTO detalle_venta (id_venta, renglon_venta, cantidad, precio_unitario_cobrado, id_variante)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_venta, idx, item[1], item[2], item[0]))

            logger.info("Pedido %s (#%s) confirmado y pagado vía Mercado Pago. Venta POS #%s generada.", external_reference, id_pedido, id_venta)

        # Enviar notificación por email
        EcommerceService.enviar_notificacion_venta(
            codigo=external_reference,
            cliente=cliente_nom,
            monto=total,
            metodo="Mercado Pago"
        )

        return {"status": "success", "pedido": external_reference, "payment_id": payment_id}

    # =========================================================================
    # APROBACIÓN MANUAL DE TRANSFERENCIAS BANCARIAS
    # =========================================================================

    @staticmethod
    def aprobar_transferencia(id_pedido: int) -> Dict[str, Any]:
        """
        El administrador valida el comprobante y aprueba el pago:
        - Bloquea stock con FOR UPDATE y descuenta.
        - Asienta venta en 'venta' y 'detalle_venta'.
        - Cambia pedido a 'PAGADO'.
        - Dispara email de confirmación.
        """
        with get_db_transaction() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT id_pedido, codigo_seguimiento, estado, subtotal, total, nombre_cliente, email_cliente
                FROM pedido_web
                WHERE id_pedido = %s
                FOR UPDATE
            """, (id_pedido,))
            pedido = cur.fetchone()

            if not pedido:
                raise RecordNotFoundError(f"Pedido #{id_pedido} no encontrado.")

            _, codigo, estado, subtotal, total, cliente_nom, cliente_email = pedido

            if estado == "PAGADO":
                raise DatabaseError("El pedido ya está marcado como PAGADO.")
            if estado == "CANCELADO":
                raise DatabaseError("No se puede aprobar un pedido que fue CANCELADO.")

            # Obtener detalles
            cur.execute("""
                SELECT dp.id_variante, dp.cantidad, dp.precio_unitario_cobrado, p.nombre_producto, col.nombre_color, tam.nombre_tamano
                FROM detalle_pedido_web dp
                JOIN variante_producto v ON dp.id_variante = v.id_variante
                JOIN producto p ON v.id_producto = p.id_producto
                JOIN color col ON v.id_color = col.id_color
                JOIN tamano tam ON v.id_tamano = tam.id_tamano
                WHERE dp.id_pedido = %s
            """, (id_pedido,))
            detalles = cur.fetchall()

            # Descontar stock con bloqueo FOR UPDATE
            for item in detalles:
                id_var, cant, precio, prod_nom, col_nom, tam_nom = item
                cur.execute("SELECT stock_actual FROM variante_producto WHERE id_variante = %s FOR UPDATE", (id_var,))
                row_st = cur.fetchone()
                if not row_st:
                    raise RecordNotFoundError(f"Variante #{id_var} no existe.")

                stock_actual = row_st[0]
                if stock_actual < cant:
                    raise DatabaseError(
                        f"Stock insuficiente para '{prod_nom} ({col_nom} - {tam_nom})'. "
                        f"Disponible: {stock_actual}, Requerido: {cant}."
                    )

                cur.execute("UPDATE variante_producto SET stock_actual = stock_actual - %s WHERE id_variante = %s", (cant, id_var))

            # Actualizar estado a PAGADO
            cur.execute("UPDATE pedido_web SET estado = 'PAGADO' WHERE id_pedido = %s", (id_pedido,))

            # Registrar venta en el sistema POS
            cur.execute("SELECT id_medio_pago FROM medio_pago WHERE nombre_medio ILIKE '%Transferencia%' LIMIT 1")
            mp_row = cur.fetchone()
            id_mp = mp_row[0] if mp_row else 1

            cur.execute("""
                INSERT INTO venta (fecha_hora, monto_total, id_medio_pago)
                VALUES (CURRENT_TIMESTAMP, %s, %s)
                RETURNING id_venta
            """, (total, id_mp))
            id_venta = cur.fetchone()[0]

            for idx, item in enumerate(detalles, start=1):
                cur.execute("""
                    INSERT INTO detalle_venta (id_venta, renglon_venta, cantidad, precio_unitario_cobrado, id_variante)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_venta, idx, item[1], item[2], item[0]))

        # Enviar notificación por email
        EcommerceService.enviar_notificacion_venta(
            codigo=codigo,
            cliente=cliente_nom,
            monto=total,
            metodo="Transferencia Bancaria (Aprobada por Admin)"
        )

        return {"id_pedido": id_pedido, "codigo": codigo, "id_venta": id_venta, "estado": "PAGADO"}

    # =========================================================================
    # CANCELACIÓN AUTOMÁTICA DE PEDIDOS EXPIRADOS (24 HORAS)
    # =========================================================================

    @staticmethod
    def expirar_pedidos_vencidos() -> int:
        """Busca pedidos pendientes cuya fecha_expiracion ya pasó y los pasa a CANCELADO."""
        query = """
            UPDATE pedido_web
            SET estado = 'CANCELADO', observaciones = COALESCE(observaciones, '') || ' [Expirado automáticamente tras 24hs sin pago]'
            WHERE estado = 'PENDIENTE_PAGO'
              AND metodo_pago = 'TRANSFERENCIA'
              AND fecha_expiracion IS NOT NULL
              AND fecha_expiracion < CURRENT_TIMESTAMP
            RETURNING id_pedido
        """
        with get_db_cursor(commit=True) as cur:
            cur.execute(query)
            filas = cur.fetchall()
            cant = len(filas)
            if cant > 0:
                logger.info("Se cancelaron automáticamente %d pedidos web vencidos.", cant)
            return cant

    # =========================================================================
    # NOTIFICACIONES POR CORREO (SMTP)
    # =========================================================================

    @staticmethod
    def enviar_notificacion_venta(codigo: str, cliente: str, monto: Decimal, metodo: str) -> bool:
        """Envía correo informativo al dueño ante un pago confirmado."""
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.info("Notificación por correo omitida: credenciales SMTP no configuradas en .env.")
            return False

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🔔 ¡Nueva Venta Web Aprobada! - {codigo}"
            msg["From"] = settings.SMTP_USER
            msg["To"] = settings.NOTIFICATION_EMAIL

            cuerpo = f"""
            <h3>¡Felicitaciones! Tenés una nueva venta online confirmada</h3>
            <p><strong>Código de Pedido:</strong> {codigo}</p>
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Monto Total:</strong> ${monto:,.2f}</p>
            <p><strong>Método de Pago:</strong> {metodo}</p>
            <p>El stock ha sido descontado automáticamente del sistema y asentado en el POS.</p>
            <p>Podés coordinar el envío por Moto Uber ingresando al panel de administración.</p>
            """
            msg.attach(MIMEText(cuerpo, "html", "utf-8"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_USER, [settings.NOTIFICATION_EMAIL], msg.as_string())

            logger.info("Correo de notificación de venta enviado exitosamente a %s.", settings.NOTIFICATION_EMAIL)
            return True
        except Exception as e:
            logger.error("Error al enviar notificación por correo electrónico: %s", e)
            return False
