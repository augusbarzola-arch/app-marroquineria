import logging
from decimal import Decimal
from typing import Dict, Any, Optional

from app.database import get_db_transaction, DatabaseError, RecordNotFoundError
from app.models.devolucion import DevolucionCreate
from app.repositories.devolucion_repo import DevolucionRepository

logger = logging.getLogger("app.services.devolucion")


class DevolucionService:
    """Lógica de negocio y transaccional para devoluciones, cambios y reparaciones."""

    @staticmethod
    def registrar_devolucion(datos: DevolucionCreate) -> int:
        """Registra la devolución y ajusta el stock según el motivo en una transacción atómica."""
        if datos.cantidad <= 0:
            raise DatabaseError("La cantidad a devolver debe ser mayor a 0.")

        with get_db_transaction() as conn:
            cursor = conn.cursor()

            # 1. Validar que la venta original y el ítem existan
            cursor.execute("""
                SELECT dv.cantidad, dv.precio_unitario_cobrado, p.nombre_producto, col.nombre_color, tam.nombre_tamano
                FROM detalle_venta dv
                JOIN variante_producto v ON dv.id_variante = v.id_variante
                JOIN producto p ON v.id_producto = p.id_producto
                JOIN color col ON v.id_color = col.id_color
                JOIN tamano tam ON v.id_tamano = tam.id_tamano
                WHERE dv.id_venta = %s AND dv.id_variante = %s
            """, (datos.id_venta, datos.id_variante_devuelta))
            detalle = cursor.fetchone()
            if not detalle:
                raise RecordNotFoundError(
                    f"El artículo seleccionado no pertenece a la venta #{datos.id_venta}."
                )

            cantidad_vendida, precio_cobrado_orig, nom_prod, col_prod, tam_prod = detalle
            precio_cobrado_original = Decimal(str(precio_cobrado_orig))

            # 2. Validar que no supere las unidades vendidas no devueltas
            cursor.execute("""
                SELECT COALESCE(SUM(cantidad), 0)
                FROM devolucion
                WHERE id_venta = %s AND id_variante_devuelta = %s
            """, (datos.id_venta, datos.id_variante_devuelta))
            ya_devueltas = cursor.fetchone()[0]

            disponibles = cantidad_vendida - ya_devueltas
            if datos.cantidad > disponibles:
                raise DatabaseError(
                    f"No se pueden devolver {datos.cantidad} unidades. "
                    f"De las {cantidad_vendida} vendidas originalmente, ya se devolvieron {ya_devueltas}. "
                    f"Máximo a devolver: {disponibles} unidad(es)."
                )

            # 3. Lógica específica según motivo
            monto_diferencia_calculado = Decimal("0.00")
            id_nueva_variante = None

            if datos.motivo == "CAMBIO":
                if not datos.id_variante_nueva:
                    raise DatabaseError("Para un CAMBIO debe especificar la nueva variante a entregar.")

                id_nueva_variante = datos.id_variante_nueva

                # Bloquear fila de la nueva variante para comprobar stock
                cursor.execute("""
                    SELECT v.stock_actual, p.precio_lista, p.nombre_producto, col.nombre_color, tam.nombre_tamano
                    FROM variante_producto v
                    JOIN producto p ON v.id_producto = p.id_producto
                    JOIN color col ON v.id_color = col.id_color
                    JOIN tamano tam ON v.id_tamano = tam.id_tamano
                    WHERE v.id_variante = %s
                    FOR UPDATE OF v
                """, (id_nueva_variante,))
                row_nueva = cursor.fetchone()
                if not row_nueva:
                    raise RecordNotFoundError("La variante nueva seleccionada no existe.")

                stock_nueva, precio_lista_nueva, nom_n, col_n, tam_n = row_nueva
                if stock_nueva < datos.cantidad:
                    raise DatabaseError(
                        f"Stock insuficiente para la variante de cambio '{nom_n} ({col_n} - {tam_n})'. "
                        f"Stock disponible: {stock_nueva}, solicitado: {datos.cantidad}."
                    )

                # Calcular monto_diferencia: (precio_variante_nueva - precio_cobrado_original) * cantidad
                precio_nueva = Decimal(str(precio_lista_nueva))
                monto_diferencia_calculado = ((precio_nueva - precio_cobrado_original) * datos.cantidad).quantize(Decimal("0.01"))

                # Ajuste de Stock CAMBIO:
                # Sumar a la devuelta y restar a la nueva
                cursor.execute("""
                    UPDATE variante_producto
                    SET stock_actual = stock_actual + %s
                    WHERE id_variante = %s
                """, (datos.cantidad, datos.id_variante_devuelta))

                cursor.execute("""
                    UPDATE variante_producto
                    SET stock_actual = stock_actual - %s
                    WHERE id_variante = %s
                """, (datos.cantidad, id_nueva_variante))

            elif datos.motivo == "DEVOLUCION":
                # id_variante_nueva debe ser NULL
                id_nueva_variante = None
                # Se reembolsa el dinero cobrado original
                monto_diferencia_calculado = Decimal("0.00")

                # Ajuste de Stock DEVOLUCION:
                # Sumar cantidad a la variante devuelta
                cursor.execute("""
                    UPDATE variante_producto
                    SET stock_actual = stock_actual + %s
                    WHERE id_variante = %s
                """, (datos.cantidad, datos.id_variante_devuelta))

            elif datos.motivo == "REPARACION":
                # id_variante_nueva debe ser NULL
                id_nueva_variante = None
                monto_diferencia_calculado = Decimal("0.00")
                # Ajuste de Stock REPARACION: NO MODIFICAR STOCK
                pass

            else:
                raise DatabaseError(f"Motivo '{datos.motivo}' no válido. Use CAMBIO, REPARACION o DEVOLUCION.")

            # 4. Insertar en tabla devolucion
            cursor.execute("""
                INSERT INTO devolucion (
                    fecha,
                    id_venta,
                    id_variante_devuelta,
                    cantidad,
                    motivo,
                    id_variante_nueva,
                    monto_diferencia,
                    observaciones
                )
                VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_devolucion
            """, (
                datos.id_venta,
                datos.id_variante_devuelta,
                datos.cantidad,
                datos.motivo,
                id_nueva_variante,
                monto_diferencia_calculado,
                datos.observaciones.strip() if datos.observaciones else None
            ))
            id_devolucion = cursor.fetchone()[0]

            cursor.close()
            logger.info("Devolución #%s registrada con éxito bajo motivo %s.", id_devolucion, datos.motivo)
            return id_devolucion

    @staticmethod
    def obtener_devolucion_completa(id_devolucion: int) -> Dict[str, Any]:
        """Obtiene el registro de devolución con datos legibles de productos devueltos y nuevos."""
        dev = DevolucionRepository.get_by_id(id_devolucion)
        if not dev:
            raise RecordNotFoundError(f"Devolución con ID {id_devolucion} no encontrada.")
        return dev
