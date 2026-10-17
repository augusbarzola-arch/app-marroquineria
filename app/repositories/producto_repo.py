from decimal import Decimal
from typing import List, Optional, Union
import psycopg2
from psycopg2.errors import ForeignKeyViolation, UniqueViolation, CheckViolation
from app.database import (
    get_db_cursor,
    ForeignKeyConstraintError,
    UniqueConstraintError,
    RecordNotFoundError,
    DatabaseError,
)


class ProductoRepository:
    """Repositorio para la tabla 'producto' usando SQL directo."""

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        id_categoria: Optional[int] = None,
        id_material: Optional[int] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[dict]:
        """Lista productos con filtros por categoría, material, término de búsqueda y datos agregados."""
        query = """
            SELECT 
                p.id_producto,
                p.sku,
                p.nombre_producto,
                p.descripcion,
                p.precio_costo,
                p.precio_lista,
                p.id_categoria,
                p.id_material,
                c.nombre_categoria,
                m.nombre_material,
                COUNT(v.id_variante) AS total_variantes,
                COALESCE(SUM(v.stock_actual), 0) AS stock_total
            FROM producto p
            JOIN categoria c ON p.id_categoria = c.id_categoria
            JOIN material m ON p.id_material = m.id_material
            LEFT JOIN variante_producto v ON p.id_producto = v.id_producto
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (p.nombre_producto ILIKE %s OR p.descripcion ILIKE %s OR p.sku ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        if id_categoria:
            query += " AND p.id_categoria = %s"
            params.append(id_categoria)

        if id_material:
            query += " AND p.id_material = %s"
            params.append(id_material)

        query += """
            GROUP BY p.id_producto, p.sku, c.nombre_categoria, m.nombre_material
            ORDER BY p.id_producto ASC
        """

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def count(
        search: Optional[str] = None,
        id_categoria: Optional[int] = None,
        id_material: Optional[int] = None
    ) -> int:
        """Cuenta total de productos que coinciden con los filtros aplicados."""
        query = """
            SELECT COUNT(*) AS total
            FROM producto p
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (p.nombre_producto ILIKE %s OR p.descripcion ILIKE %s OR p.sku ILIKE %s)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term])

        if id_categoria:
            query += " AND p.id_categoria = %s"
            params.append(id_categoria)

        if id_material:
            query += " AND p.id_material = %s"
            params.append(id_material)

        with get_db_cursor() as cur:
            cur.execute(query, tuple(params))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def get_by_id(id_producto: int) -> Optional[dict]:
        """Obtiene un producto específico por ID con datos de categoría y material."""
        query = """
            SELECT 
                p.id_producto,
                p.sku,
                p.nombre_producto,
                p.descripcion,
                p.precio_costo,
                p.precio_lista,
                p.id_categoria,
                p.id_material,
                c.nombre_categoria,
                m.nombre_material
            FROM producto p
            JOIN categoria c ON p.id_categoria = c.id_categoria
            JOIN material m ON p.id_material = m.id_material
            WHERE p.id_producto = %s
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_producto,))
            row = cur.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_variantes(id_producto: int) -> List[dict]:
        """Obtiene todas las variantes de un producto con nombres de color y tamaño."""
        query = """
            SELECT 
                v.id_variante,
                v.id_producto,
                v.id_color,
                v.id_tamano,
                v.stock_actual,
                v.stock_minimo,
                col.nombre_color,
                tam.nombre_tamano
            FROM variante_producto v
            JOIN color col ON v.id_color = col.id_color
            JOIN tamano tam ON v.id_tamano = tam.id_tamano
            WHERE v.id_producto = %s
            ORDER BY v.id_variante ASC
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_producto,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def create(
        nombre_producto: str,
        descripcion: Optional[str],
        precio_costo: Union[float, Decimal],
        precio_lista: Union[float, Decimal],
        id_categoria: int,
        id_material: int,
        sku: Optional[str] = None
    ) -> int:
        """Inserta un nuevo producto y retorna el ID autogenerado. Si sku no se provee, autogenera PROD-###."""
        clean_sku = sku.strip() if (sku and sku.strip()) else None
        query = """
            INSERT INTO producto (
                sku,
                nombre_producto,
                descripcion,
                precio_costo,
                precio_lista,
                id_categoria,
                id_material
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_producto
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (
                    clean_sku,
                    nombre_producto.strip(),
                    descripcion.strip() if descripcion else None,
                    precio_costo,
                    precio_lista,
                    id_categoria,
                    id_material
                ))
                row = cur.fetchone()
                new_id = row["id_producto"]
                if not clean_sku:
                    auto_sku = f"PROD-{new_id:03d}"
                    cur.execute("UPDATE producto SET sku = %s WHERE id_producto = %s;", (auto_sku, new_id))
                return new_id
        except UniqueViolation as e:
            raise UniqueConstraintError(f"El SKU '{clean_sku}' ya está registrado en otro producto.") from e
        except CheckViolation as e:
            raise DatabaseError("Los precios no pueden ser negativos.") from e
        except ForeignKeyViolation as e:
            raise DatabaseError("La categoría o el material especificado no existe.") from e

    @staticmethod
    def update(
        id_producto: int,
        nombre_producto: str,
        descripcion: Optional[str],
        precio_costo: Union[float, Decimal],
        precio_lista: Union[float, Decimal],
        id_categoria: int,
        id_material: int,
        sku: Optional[str] = None
    ) -> bool:
        """Actualiza un producto existente."""
        clean_sku = sku.strip() if (sku and sku.strip()) else f"PROD-{id_producto:03d}"
        query = """
            UPDATE producto
            SET sku = %s,
                nombre_producto = %s,
                descripcion = %s,
                precio_costo = %s,
                precio_lista = %s,
                id_categoria = %s,
                id_material = %s
            WHERE id_producto = %s
        """
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (
                    clean_sku,
                    nombre_producto.strip(),
                    descripcion.strip() if descripcion else None,
                    precio_costo,
                    precio_lista,
                    id_categoria,
                    id_material,
                    id_producto
                ))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Producto con ID {id_producto} no encontrado.")
                return True
        except UniqueViolation as e:
            raise UniqueConstraintError(f"El SKU '{clean_sku}' ya está registrado en otro producto.") from e
        except CheckViolation as e:
            raise DatabaseError("Los precios no pueden ser negativos.") from e
        except ForeignKeyViolation as e:
            raise DatabaseError("La categoría o el material especificado no existe.") from e

    @staticmethod
    def count_references(id_producto: int) -> int:
        """Cuenta si alguna de las variantes del producto posee operaciones en ventas, compras o devoluciones."""
        query = """
            SELECT (
                (SELECT COUNT(*) FROM detalle_venta dv 
                 JOIN variante_producto vp ON dv.id_variante = vp.id_variante 
                 WHERE vp.id_producto = %s) +
                (SELECT COUNT(*) FROM detalle_compra dc 
                 JOIN variante_producto vp ON dc.id_variante = vp.id_variante 
                 WHERE vp.id_producto = %s) +
                (SELECT COUNT(*) FROM devolucion d 
                 JOIN variante_producto vp ON (d.id_variante_devuelta = vp.id_variante OR d.id_variante_nueva = vp.id_variante)
                 WHERE vp.id_producto = %s)
            ) AS total
        """
        with get_db_cursor() as cur:
            cur.execute(query, (id_producto, id_producto, id_producto))
            row = cur.fetchone()
            return row["total"] if row else 0

    @staticmethod
    def delete(id_producto: int) -> bool:
        """Elimina un producto y sus variantes (en cascada) si ninguna de sus variantes está en uso."""
        refs = ProductoRepository.count_references(id_producto)
        if refs > 0:
            raise ForeignKeyConstraintError(
                f"No se puede eliminar porque sus variantes están siendo usadas por {refs} operaciones registradas.",
                count=refs
            )

        query = "DELETE FROM producto WHERE id_producto = %s"
        try:
            with get_db_cursor(commit=True) as cur:
                cur.execute(query, (id_producto,))
                if cur.rowcount == 0:
                    raise RecordNotFoundError(f"Producto con ID {id_producto} no encontrado.")
                return True
        except ForeignKeyViolation as e:
            raise ForeignKeyConstraintError(
                "No se puede eliminar porque está siendo referenciado por otros registros.",
                count=refs
            ) from e
