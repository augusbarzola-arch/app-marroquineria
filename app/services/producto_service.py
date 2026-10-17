import logging
from decimal import Decimal
from typing import Optional, Tuple, Dict, Any

from app.models.producto import ProductoCreate, ProductoUpdate
from app.models.variante import VarianteCreate, VarianteUpdate
from app.repositories.producto_repo import ProductoRepository
from app.repositories.variante_repo import VarianteRepository
from app.database import RecordNotFoundError

logger = logging.getLogger("app.services.producto")


class ProductoService:
    """Lógica de negocio para productos y sus variantes asociadas."""

    @staticmethod
    def crear_producto(datos: ProductoCreate) -> Tuple[int, Optional[str]]:
        """Registra un producto. Si precio_lista < precio_costo, genera advertencia pero permite la creación."""
        advertencia = None
        if datos.precio_lista < datos.precio_costo:
            advertencia = (
                f"Advertencia: El precio de lista (${datos.precio_lista:.2f}) "
                f"es menor que el precio de costo (${datos.precio_costo:.2f})."
            )
            logger.warning("Creando producto '%s' con margen negativo: %s", datos.nombre_producto, advertencia)

        id_producto = ProductoRepository.create(
            nombre_producto=datos.nombre_producto,
            descripcion=datos.descripcion,
            precio_costo=datos.precio_costo,
            precio_lista=datos.precio_lista,
            id_categoria=datos.id_categoria,
            id_material=datos.id_material,
            sku=datos.sku
        )
        return id_producto, advertencia

    @staticmethod
    def actualizar_producto(id_producto: int, datos: ProductoUpdate) -> Tuple[bool, Optional[str]]:
        """Actualiza un producto existente y emite advertencia si el margen es negativo."""
        advertencia = None
        if datos.precio_lista < datos.precio_costo:
            advertencia = (
                f"Advertencia: El precio de lista (${datos.precio_lista:.2f}) "
                f"es menor que el precio de costo (${datos.precio_costo:.2f})."
            )

        ProductoRepository.update(
            id_producto=id_producto,
            nombre_producto=datos.nombre_producto,
            descripcion=datos.descripcion,
            precio_costo=datos.precio_costo,
            precio_lista=datos.precio_lista,
            id_categoria=datos.id_categoria,
            id_material=datos.id_material,
            sku=datos.sku
        )
        return True, advertencia

    @staticmethod
    def obtener_detalle(id_producto: int) -> Dict[str, Any]:
        """Obtiene datos completos del producto, lista de variantes y métricas de margen."""
        producto = ProductoRepository.get_by_id(id_producto)
        if not producto:
            raise RecordNotFoundError(f"Producto con ID {id_producto} no encontrado.")

        variantes = ProductoRepository.get_variantes(id_producto)

        # Cálculo del margen porcentual de ganancia
        costo = Decimal(str(producto["precio_costo"]))
        lista = Decimal(str(producto["precio_lista"]))
        margen = 0.0
        if costo > 0:
            margen = float(((lista - costo) / costo) * 100)

        total_stock = sum(v["stock_actual"] for v in variantes)

        return {
            "producto": producto,
            "variantes": variantes,
            "margen_porcentaje": round(margen, 2),
            "total_stock": total_stock,
            "total_variantes": len(variantes)
        }

    @staticmethod
    def crear_variante(datos: VarianteCreate) -> int:
        """Crea una variante vinculada al producto."""
        return VarianteRepository.create(
            id_producto=datos.id_producto,
            id_color=datos.id_color,
            id_tamano=datos.id_tamano,
            stock_actual=datos.stock_actual,
            stock_minimo=datos.stock_minimo
        )

    @staticmethod
    def actualizar_variante(
        id_variante: int,
        id_color: int,
        id_tamano: int,
        stock_actual: int,
        stock_minimo: int
    ) -> bool:
        """Actualiza atributos de la variante."""
        return VarianteRepository.update(
            id_variante=id_variante,
            id_color=id_color,
            id_tamano=id_tamano,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo
        )

    @staticmethod
    def eliminar_variante(id_variante: int) -> bool:
        """Elimina una variante si no está en uso."""
        return VarianteRepository.delete(id_variante)

    @staticmethod
    def eliminar_producto(id_producto: int) -> bool:
        """Elimina un producto y sus variantes si ninguna está en uso."""
        return ProductoRepository.delete(id_producto)
