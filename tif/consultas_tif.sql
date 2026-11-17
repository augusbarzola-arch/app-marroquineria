-- ============================================================
-- CONSULTAS TIF 2 - Sistema Marroquinería
-- 8 consultas con operaciones avanzadas + consulta de 3
-- tablas con igualdad y rango, con desarrollo algebraico.
-- ============================================================


-- ============================================================
-- CONSULTA 1: Stock por producto, color y talle
-- Tipo: JOIN (4 tablas)
-- ============================================================
SELECT p.nombre_producto,
       c.nombre_color,
       t.nombre_tamano,
       v.stock_actual,
       v.stock_minimo
FROM variante_producto v
JOIN producto p ON p.id_producto = v.id_producto
JOIN color    c ON c.id_color    = v.id_color
JOIN tamano   t ON t.id_tamano   = v.id_tamano
ORDER BY p.nombre_producto, c.nombre_color, t.nombre_tamano;


-- ============================================================
-- CONSULTA 2: Variantes con stock por debajo del mínimo
-- Tipo: JOIN (4 tablas) + comparación entre columnas
-- ============================================================
SELECT p.nombre_producto,
       c.nombre_color,
       t.nombre_tamano,
       v.stock_actual,
       v.stock_minimo
FROM variante_producto v
JOIN producto p ON p.id_producto = v.id_producto
JOIN color    c ON c.id_color    = v.id_color
JOIN tamano   t ON t.id_tamano   = v.id_tamano
WHERE v.stock_actual <= v.stock_minimo
ORDER BY p.nombre_producto;


-- ============================================================
-- CONSULTA 3: Ventas del último día con actividad
-- Tipo: JOIN (2 tablas) + subconsulta escalar
-- ============================================================
SELECT v.id_venta,
       v.fecha_hora,
       mp.nombre_medio,
       v.monto_total
FROM venta v
JOIN medio_pago mp ON mp.id_medio_pago = v.id_medio_pago
WHERE DATE(v.fecha_hora) = (SELECT MAX(DATE(fecha_hora)) FROM venta)
ORDER BY v.fecha_hora;


-- ============================================================
-- CONSULTA 4: Devoluciones del último mes con actividad
-- Tipo: JOIN (5 tablas) usando la FK compuesta
--       (id_venta, renglon_venta) → detalle_venta
-- ============================================================
SELECT d.id_devolucion,
       d.fecha,
       d.motivo,
       p.nombre_producto,
       c.nombre_color,
       d.cantidad,
       d.monto_diferencia
FROM devolucion d
JOIN detalle_venta      dv ON dv.id_venta      = d.id_venta
                           AND dv.renglon_venta = d.renglon_venta
JOIN variante_producto  v  ON v.id_variante    = dv.id_variante
JOIN producto           p  ON p.id_producto    = v.id_producto
JOIN color              c  ON c.id_color       = v.id_color
WHERE DATE_TRUNC('month', d.fecha) = (
    SELECT DATE_TRUNC('month', MAX(fecha)) FROM devolucion
)
ORDER BY d.fecha;


-- ============================================================
-- CONSULTA 5: Productos que se vendieron al menos una vez
-- Tipo: EXISTS (subconsulta correlacionada)
-- ============================================================
SELECT p.id_producto,
       p.nombre_producto,
       p.precio_lista
FROM producto p
WHERE EXISTS (
    SELECT 1
    FROM variante_producto v
    JOIN detalle_venta dv ON dv.id_variante = v.id_variante
    WHERE v.id_producto = p.id_producto
)
ORDER BY p.nombre_producto;


-- ============================================================
-- CONSULTA 6: Variantes que NUNCA se vendieron
-- Tipo: NOT EXISTS
-- ============================================================
SELECT v.id_variante,
       p.nombre_producto,
       c.nombre_color,
       t.nombre_tamano,
       v.stock_actual
FROM variante_producto v
JOIN producto p ON p.id_producto = v.id_producto
JOIN color    c ON c.id_color    = v.id_color
JOIN tamano   t ON t.id_tamano   = v.id_tamano
WHERE NOT EXISTS (
    SELECT 1
    FROM detalle_venta dv
    WHERE dv.id_variante = v.id_variante
)
ORDER BY p.nombre_producto, c.nombre_color;


-- ============================================================
-- CONSULTA 7: Productos con al menos una variante sin stock
-- Tipo: IN (subconsulta)
-- ============================================================
SELECT p.id_producto,
       p.nombre_producto,
       p.precio_lista
FROM producto p
WHERE p.id_producto IN (
    SELECT v.id_producto
    FROM variante_producto v
    WHERE v.stock_actual = 0
)
ORDER BY p.nombre_producto;


-- ============================================================
-- CONSULTA 8: Categorías con más de 4 productos distintos
-- Tipo: GROUP BY + HAVING + JOIN
-- ============================================================
SELECT c.id_categoria,
       c.nombre_categoria,
       COUNT(p.id_producto) AS cantidad_productos
FROM categoria c
JOIN producto p ON p.id_categoria = c.id_categoria
GROUP BY c.id_categoria, c.nombre_categoria
HAVING COUNT(p.id_producto) > 4
ORDER BY cantidad_productos DESC;


-- ============================================================
-- ============================================================
-- CONSULTA ESPECIAL (consigna punto 3):
-- Tres tablas + condición de igualdad + condición de rango
--
-- Enunciado: "Listar los productos de la categoría 'Mochilas y Monomochilas'
-- que tienen variantes con stock_actual > 20"
-- ============================================================
-- ============================================================


-- ------------------------------------------------------------
-- 8.1. CONSULTA SQL ORIGINAL (forma canónica con producto cartesiano)
-- ------------------------------------------------------------
SELECT p.nombre_producto,
       c.nombre_categoria,
       v.stock_actual
FROM producto p, categoria c, variante_producto v
WHERE p.id_categoria = c.id_categoria          -- igualdad (enlace)
  AND v.id_producto  = p.id_producto           -- igualdad (enlace)
  AND c.nombre_categoria = 'Mochilas y Monomochilas' -- igualdad (filtro)
  AND v.stock_actual > 20;                     -- rango >


-- ------------------------------------------------------------
-- 8.2. ÁRBOL DE EJECUCIÓN SIN OPTIMIZAR (Álgebra Relacional Canónica)
--
-- Expresión formal:
--   π [ p.nombre_producto, c.nombre_categoria, v.stock_actual ]
--     |
--     σ [ c.nombre_categoria = 'Mochilas y Monomochilas' ∧ v.stock_actual > 20
--         ∧ p.id_categoria = c.id_categoria ∧ v.id_producto = p.id_producto ]
--       |
--       ×
--      / \
--     ×   [ variante_producto v ]  (|V| = 26)
--    / \
-- [ producto p ] [ categoria c ]  (|P| = 16, |C| = 6)
--
-- Costo Intermedio Real en la Base:
--   |P| × |C| × |V| = 16 × 6 × 26 = 2.496 tuplas intermedias.
-- Se calcula el producto cartesiano total y se filtran todas las
-- condiciones en la raíz del árbol.
-- ------------------------------------------------------------


-- ------------------------------------------------------------
-- 8.3. OPTIMIZACIÓN DEL ÁRBOL (Reglas de Equivalencia Formal)
--
-- Reglas aplicadas según lo enseñado en clase:
--   1. Push-Down de Selecciones (σ): Bajar las condiciones unarias
--      lo más cerca posible de las hojas del árbol.
--      - σ [ c.nombre_categoria = 'Mochilas y Monomochilas' ] sobre categoria (de 6 a 1 tupla).
--      - σ [ v.stock_actual > 20 ] sobre variante_producto (de 26 a 6 tuplas).
--
--   2. Push-Down de Proyecciones (π): Proyectar tempranamente solo los
--      atributos indispensables para los enlaces posteriores y la salida final,
--      descartando atributos irrelevantes (costo, descripción, etc.).
--      - Sobre Categoria: π [ id_categoria, nombre_categoria ]
--      - Sobre Producto: π [ id_producto, id_categoria, nombre_producto ]
--      - Sobre Variante: π [ id_producto, stock_actual ]
--
--   3. Sustituir Producto Cartesiano por JOIN (⋈): Convertir los productos
--      cartesianos en reuniones naturales usando las claves foráneas.
--
-- ÁRBOL OPTIMIZADO FORMAL:
--
--   π [ p.nombre_producto, c.nombre_categoria, v.stock_actual ]
--     |
--     ⋈ [ v.id_producto = p.id_producto ]
--     /                              \
--   π [ id_producto, stock_actual ]   π [ id_producto, nombre_producto, c.nombre_categoria ]
--     |                                 |
--   σ [ v.stock_actual > 20 ]           ⋈ [ p.id_categoria = c.id_categoria ]
--     |                                /                              \
--   [ variante_producto v ]     π [ id_producto, id_categoria,   π [ id_categoria, nombre_categoria ]
--                                   nombre_producto ]              |
--                                       |                        σ [ c.nombre_categoria = 'Mochilas y Monomochilas' ]
--                                 [ producto p ]                   |
--                                                            [ categoria c ]
--
-- Costo Intermedio Optimizado:
--   - Categoria filtrada y proyectada: 1 tupla.
--   - Join Categoria ⋈ Producto: 5 tuplas (solo los 5 productos de Mochilas).
--   - Variante filtrada y proyectada (stock > 20): 6 tuplas.
--   - Join final: 6 tuplas.
--   De 2.496 tuplas cartesianas se reduce a menos de 20 tuplas intermedias.
-- ------------------------------------------------------------


-- ------------------------------------------------------------
-- 8.4. CONSULTA SQL OPTIMIZADA (Siguiendo la estructura del árbol)
-- ------------------------------------------------------------
SELECT p.nombre_producto,
       c.nombre_categoria,
       v.stock_actual
FROM (
    SELECT id_categoria, nombre_categoria
    FROM categoria
    WHERE nombre_categoria = 'Mochilas y Monomochilas'  -- Selección bajada a C
) c
JOIN (
    SELECT id_producto, id_categoria, nombre_producto
    FROM producto                                      -- Proyección bajada a P
) p ON p.id_categoria = c.id_categoria
JOIN (
    SELECT id_producto, stock_actual
    FROM variante_producto
    WHERE stock_actual > 20                             -- Selección bajada a V
) v ON v.id_producto = p.id_producto
ORDER BY p.nombre_producto, v.stock_actual DESC;
