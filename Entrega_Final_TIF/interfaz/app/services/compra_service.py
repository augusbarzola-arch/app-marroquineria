import logging
from decimal import Decimal
from typing import Dict, Any, List

from app.database import get_db_transaction, DatabaseError, RecordNotFoundError
from app.models.compra import CompraCreate
from app.repositories.compra_repo import CompraRepository

logger = logging.getLogger("app.services.compra")


class CompraService:
    """Lógica de negocio y transaccional para la gestión de compras a proveedores."""

    @staticmethod
    def registrar_compra(datos: CompraCreate) -> int:
        """Registra una orden de compra, sus renglones y SUMA el stock a cada variante en una transacción atómica."""
        if not datos.items:
            raise DatabaseError("La orden de compra debe contener al menos un ítem.")

        with get_db_transaction() as conn:
            cursor = conn.cursor()

            # 1. Verificar proveedor
            cursor.execute(
                "SELECT id_proveedor, razon_social FROM proveedor WHERE id_proveedor = %s",
                (datos.id_proveedor,)
            )
            prov = cursor.fetchone()
            if not prov:
                raise RecordNotFoundError(f"Proveedor con ID {datos.id_proveedor} no encontrado.")

            # 2. Validar ítems y calcular total
            items_procesados = []
            monto_total_calculado = Decimal("0.00")

            for item in datos.items:
                if item.cantidad <= 0:
                    raise DatabaseError("La cantidad comprada de cada ítem debe ser mayor a 0.")
                if item.precio_costo_unitario < Decimal("0.00"):
                    raise DatabaseError("El precio de costo unitario no puede ser negativo.")

                cursor.execute("""
                    SELECT v.id_variante, v.stock_actual, p.nombre_producto, col.nombre_color, tam.nombre_tamano
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

                id_var, stock_actual, nombre_prod, col_nom, tam_nom = row
                subtotal_item = (item.precio_costo_unitario * item.cantidad).quantize(Decimal("0.01"))
                monto_total_calculado += subtotal_item

                items_procesados.append({
                    "id_variante": id_var,
                    "cantidad": item.cantidad,
                    "precio_costo_unitario": item.precio_costo_unitario,
                    "stock_nuevo": stock_actual + item.cantidad  # SUMA STOCK
                })

            # 3. Insertar registro cabecera en compra
            cursor.execute("""
                INSERT INTO compra (fecha_compra, monto_total, id_proveedor)
                VALUES (CURRENT_TIMESTAMP, %s, %s)
                RETURNING id_compra
            """, (monto_total_calculado, datos.id_proveedor))
            id_compra = cursor.fetchone()[0]

            # 4. Insertar renglones en detalle_compra y SUMAR stock a cada variante
            for idx, item in enumerate(items_procesados, start=1):
                cursor.execute("""
                    INSERT INTO detalle_compra (id_compra, renglon_compra, cantidad, precio_costo_unitario, id_variante)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_compra, idx, item["cantidad"], item["precio_costo_unitario"], item["id_variante"]))

                cursor.execute("""
                    UPDATE variante_producto
                    SET stock_actual = %s
                    WHERE id_variante = %s
                """, (item["stock_nuevo"], item["id_variante"]))

            cursor.close()
            logger.info("Compra #%s registrada con éxito. Total: $%s", id_compra, monto_total_calculado)
            return id_compra

    @staticmethod
    def obtener_compra_completa(id_compra: int) -> Dict[str, Any]:
        """Obtiene la orden de compra con datos de proveedor y lista de ítems comprados."""
        compra = CompraRepository.get_by_id(id_compra)
        if not compra:
            raise RecordNotFoundError(f"Compra con ID {id_compra} no encontrada.")

        detalles = CompraRepository.get_detalles(id_compra)

        return {
            "compra": compra,
            "detalles": detalles,
            "total_unidades": sum(d["cantidad"] for d in detalles)
        }
