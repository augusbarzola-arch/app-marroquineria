import logging
from decimal import Decimal
from typing import Dict, Any, List

from app.database import get_db_transaction, DatabaseError, RecordNotFoundError
from app.models.venta import VentaCreate
from app.repositories.venta_repo import VentaRepository

logger = logging.getLogger("app.services.venta")


class VentaService:
    """Lógica de negocio y transaccional para la gestión de ventas."""

    @staticmethod
    def registrar_venta(datos: VentaCreate) -> int:
        """Registra una venta completa con sus detalles y descuento de stock dentro de una transacción atómica."""
        if not datos.items:
            raise DatabaseError("La venta debe contener al menos un producto en el carrito.")

        with get_db_transaction() as conn:
            cursor = conn.cursor()

            # 1. Verificar existencia y ajuste del medio de pago
            cursor.execute(
                "SELECT id_medio_pago, nombre_medio, porcentaje_descuento_recargo FROM medio_pago WHERE id_medio_pago = %s",
                (datos.id_medio_pago,)
            )
            mp = cursor.fetchone()
            if not mp:
                raise RecordNotFoundError(f"Medio de pago con ID {datos.id_medio_pago} no encontrado.")

            pct = Decimal(str(mp[2]))  # porcentaje_descuento_recargo
            factor = Decimal("1.0") + (pct / Decimal("100.0"))

            # 2. Validar stock de cada variante con bloqueo de fila (FOR UPDATE)
            items_procesados = []
            monto_total_calculado = Decimal("0.00")

            for item in datos.items:
                if item.cantidad <= 0:
                    raise DatabaseError("La cantidad vendida de cada ítem debe ser mayor a 0.")

                cursor.execute("""
                    SELECT 
                        v.id_variante, 
                        v.stock_actual, 
                        p.nombre_producto, 
                        p.precio_lista, 
                        col.nombre_color, 
                        tam.nombre_tamano
                    FROM variante_producto v
                    JOIN producto p ON v.id_producto = p.id_producto
                    JOIN color col ON v.id_color = col.id_color
                    JOIN tamano tam ON v.id_tamano = tam.id_tamano
                    WHERE v.id_variante = %s
                    FOR UPDATE OF v
                """, (item.id_variante,))
                row = cursor.fetchone()
                if not row:
                    raise RecordNotFoundError(f"Variante con ID {item.id_variante} no encontrada.")

                id_var, stock_actual, nombre_prod, precio_lista, col_nom, tam_nom = row

                # Validación de stock suficiente
                if stock_actual < item.cantidad:
                    raise DatabaseError(
                        f"Stock insuficiente para '{nombre_prod} ({col_nom} - {tam_nom})'. "
                        f"Disponible: {stock_actual} unidad(es), Solicitado: {item.cantidad}."
                    )

                precio_lista_dec = Decimal(str(precio_lista))
                precio_cobrado = (precio_lista_dec * factor).quantize(Decimal("0.01"))
                subtotal_item = precio_cobrado * item.cantidad
                monto_total_calculado += subtotal_item

                items_procesados.append({
                    "id_variante": id_var,
                    "cantidad": item.cantidad,
                    "precio_unitario_cobrado": precio_cobrado,
                    "stock_nuevo": stock_actual - item.cantidad
                })

            # 3. Insertar registro cabecera en venta
            cursor.execute("""
                INSERT INTO venta (fecha_hora, monto_total, id_medio_pago)
                VALUES (CURRENT_TIMESTAMP, %s, %s)
                RETURNING id_venta
            """, (monto_total_calculado, datos.id_medio_pago))
            id_venta = cursor.fetchone()[0]

            # 4. Insertar cada ítem en detalle_venta y descontar el stock
            for idx, item in enumerate(items_procesados, start=1):
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, renglon_venta, cantidad, precio_unitario_cobrado, id_variante)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_venta, idx, item["cantidad"], item["precio_unitario_cobrado"], item["id_variante"]))

                cursor.execute("""
                    UPDATE variante_producto
                    SET stock_actual = %s
                    WHERE id_variante = %s
                """, (item["stock_nuevo"], item["id_variante"]))

            cursor.close()
            logger.info("Venta #%s registrada con éxito. Total: $%s", id_venta, monto_total_calculado)
            return id_venta

    @staticmethod
    def obtener_venta_completa(id_venta: int) -> Dict[str, Any]:
        """Obtiene la venta con su medio de pago y la lista de ítems detallados."""
        venta = VentaRepository.get_by_id(id_venta)
        if not venta:
            raise RecordNotFoundError(f"Venta con ID {id_venta} no encontrada.")

        detalles = VentaRepository.get_detalles(id_venta)
        subtotal_original = sum(Decimal(str(d["precio_lista_original"])) * d["cantidad"] for d in detalles)
        descuento_recargo_monto = Decimal(str(venta["monto_total"])) - subtotal_original

        return {
            "venta": venta,
            "detalles": detalles,
            "subtotal_original": subtotal_original,
            "descuento_recargo_monto": descuento_recargo_monto,
            "total_unidades": sum(d["cantidad"] for d in detalles)
        }
