-- ============================================================
-- DML - POBLADO DE DATOS CORREGIDO Y ENRIQUECIDO
-- Sistema de Gestión Comercial - Marroquinería
-- ============================================================

TRUNCATE TABLE devolucion, detalle_venta, detalle_compra, venta, compra, 
               variante_producto, producto, color, tamano, categoria, 
               material, proveedor, medio_pago RESTART IDENTITY CASCADE;

-- 1. CATEGORIAS (6)
INSERT INTO categoria (id_categoria, nombre_categoria, descripcion) VALUES
(1, 'Billeteras', 'Billeteras y tarjeteros de dama y hombre'),
(2, 'Mochilas y Monomochilas', 'Mochilas urbanas, ejecutivas e infantiles'),
(3, 'Valijas y Viaje', 'Valijas rígidas, blandas y bolsos de viaje'),
(4, 'Carteras y Bolsos', 'Carteras de mano, bandoleras y bolsos deportivos'),
(5, 'Riñoneras y Portafolios', 'Riñoneras para dama/hombre y portafolios de trabajo'),
(6, 'Electrónica y Accesorios', 'Accesorios complementarios, vasos térmicos y gadgets');

-- 2. MATERIALES (5)
INSERT INTO material (id_material, nombre_material) VALUES
(1, 'Cuero Vacuno'),
(2, 'Cuero Sintético / PU'),
(3, 'Lona / Cordura'),
(4, 'Poliéster / Nylon'),
(5, 'Acero Inoxidable');

-- 3. COLORES (6)
INSERT INTO color (id_color, nombre_color) VALUES
(1, 'Negro'),
(2, 'Azul'),
(3, 'Rojo'),
(4, 'Marrón'),
(5, 'Beige'),
(6, 'Único');

-- 4. TAMAÑOS (4)
INSERT INTO tamano (id_tamano, nombre_tamano) VALUES
(1, 'Grande'),
(2, 'Chica'),
(3, 'Mediano'),
(4, 'Único');

-- 5. PRODUCTOS (16) - Categoria 2 tiene 5 productos (>4 para Consulta 8)
INSERT INTO producto (id_producto, nombre_producto, descripcion, precio_costo, precio_lista, id_categoria, id_material) VALUES
-- Categoria 1: Billeteras (3 productos)
(1, 'Billetera Hombre Clásica', 'Billetera de cuero con tarjetero y billetero', 8000.00, 16000.00, 1, 1),
(2, 'Billetera Dama Cierre Cuerina', 'Billetera espaciosa con cierre perimetral', 6500.00, 13000.00, 1, 2),
(3, 'Billetera Tarjetero Slim', 'Tarjetero compacto de bolsillo', 4000.00, 8500.00, 1, 1),
-- Categoria 2: Mochilas y Monomochilas (5 productos -> HAVING > 4)
(4, 'Mochila Urbana Porta Notebook', 'Mochila reforzada acolchada para laptop 15.6', 22000.00, 44000.00, 2, 4),
(5, 'Monomochila Infantil', 'Monomochila pequeña cruzada para niños', 9000.00, 18000.00, 2, 3),
(6, 'Mochila Antirrobo Ejecutiva', 'Mochila impermeable con cierre oculto y puerto USB', 26000.00, 52000.00, 2, 4),
(7, 'Mochila Escolar Reforzada', 'Mochila de gran capacidad con base plástica', 18000.00, 36000.00, 2, 3),
(8, 'Monomochila Deportiva Táctica', 'Bolso cruzado táctico con sistema molle', 12000.00, 24000.00, 2, 4),
-- Categoria 3: Valijas y Viaje (2 productos)
(9, 'Valija 24 Rígida Carry On', 'Valija de cabina 4 ruedas 360 grados', 45000.00, 90000.00, 3, 2),
(10, 'Bolso Valija de Mano Plegable', 'Bolso carry on con fuelle expansible', 20000.00, 40000.00, 3, 4),
-- Categoria 4: Carteras y Bolsos (2 productos)
(11, 'Cartera Bandolera de Cuero', 'Cartera de hombro con apliques metálicos', 28000.00, 56000.00, 4, 1),
(12, 'Bolso Deportivo 50L', 'Bolso amplio para gimnasio o viaje corto', 15000.00, 30000.00, 4, 3),
-- Categoria 5: Riñoneras y Portafolios (2 productos)
(13, 'Riñonera Urbana Unisex', 'Riñonera con triple compartimento', 7500.00, 15000.00, 5, 4),
(14, 'Portafolio Ejecutivo Cuero', 'Portafolio clásico con cerradura y fuelle', 35000.00, 70000.00, 5, 1),
-- Categoria 6: Electrónica y Accesorios (2 productos)
(15, 'Vaso Térmico 500ml', 'Vaso de acero inoxidable frío/calor', 5000.00, 10000.00, 6, 5),
(16, 'Organizador Cables y Accesorios', 'Estuche organizador de viaje para cables', 4500.00, 9000.00, 6, 4);

-- 6. VARIANTES DE PRODUCTO (26)
-- Con stock > 20 para consulta álgebra, con stock = 0 para Consulta 7, y con stock <= stock_minimo para Consulta 2
INSERT INTO variante_producto (id_variante, id_producto, id_color, id_tamano, stock_actual, stock_minimo) VALUES
-- Variantes Billeteras
(1, 1, 4, 4, 25, 5),   -- Billetera Hombre Marrón Único
(2, 1, 1, 4, 15, 5),   -- Billetera Hombre Negro Único
(3, 2, 5, 4, 18, 5),   -- Billetera Dama Beige Único
(4, 3, 1, 4, 30, 8),   -- Billetera Slim Negra Único
-- Variantes Mochilas y Monomochilas (Varios con stock > 20 para Álgebra Relacional)
(5, 4, 1, 4, 28, 5),   -- Mochila Porta Notebook Negra Único (stock > 20)
(6, 4, 2, 4, 24, 5),   -- Mochila Porta Notebook Azul Único (stock > 20)
(7, 4, 3, 4, 2, 3),    -- Mochila Porta Notebook Roja Único (stock <= min)
(8, 5, 6, 4, 35, 6),   -- Monomochila Infantil Único Único (stock > 20)
(9, 6, 1, 4, 22, 5),   -- Mochila Antirrobo Negra Único (stock > 20)
(10, 7, 2, 4, 26, 5),  -- Mochila Escolar Azul Único (stock > 20)
(11, 8, 1, 4, 14, 4),  -- Monomochila Táctica Negra Único
-- Variantes Valijas
(12, 9, 1, 1, 3, 2),   -- Valija Negra Grande
(13, 9, 1, 2, 0, 2),   -- Valija Negra Chica (stock = 0 -> Consulta 7)
(14, 10, 2, 3, 8, 3),  -- Bolso Valija Azul Mediano
-- Variantes Carteras y Bolsos
(15, 11, 4, 4, 10, 3), -- Cartera Cuero Marrón Único
(16, 11, 1, 4, 1, 3),  -- Cartera Cuero Negra Único (stock <= min -> Consulta 2)
(17, 12, 1, 4, 14, 4), -- Bolso Deportivo Negro Único
(18, 12, 2, 4, 9, 3),  -- Bolso Deportivo Azul Único
-- Variantes Riñoneras y Portafolios
(19, 13, 1, 4, 12, 5), -- Riñonera Negra Único
(20, 13, 2, 4, 8, 5),  -- Riñonera Azul Único
(21, 13, 3, 4, 2, 5),  -- Riñonera Roja Único (stock <= min -> Consulta 2)
(22, 14, 4, 4, 4, 1),  -- Portafolio Marrón Único (NUNCA VENDIDO -> Consulta 6)
(23, 14, 1, 4, 3, 1),  -- Portafolio Negro Único (NUNCA VENDIDO -> Consulta 6)
-- Variantes Accesorios
(24, 15, 6, 4, 40, 8), -- Vaso Térmico Único Único
(25, 16, 1, 4, 0, 3),  -- Organizador Negro Único (stock = 0 -> Consulta 7)
(26, 16, 2, 4, 15, 3); -- Organizador Azul Único

-- 7. PROVEEDORES (3)
INSERT INTO proveedor (id_proveedor, cuit, razon_social, telefono, email) VALUES
(1, '30-71123456-8', 'Taller Marroquí S.A.', '1140001111', 'ventas@tallermarroqui.com'),
(2, '30-68987654-2', 'Importadora BagStyle SRL', '1142223333', 'contacto@bagstyle.com'),
(3, '30-54321876-5', 'Distribuidora del Cuero Argentina', '1144445555', 'pedidos@distdelcuero.com');

-- 8. MEDIOS DE PAGO (4)
INSERT INTO medio_pago (id_medio_pago, nombre_medio, porcentaje_descuento_recargo) VALUES
(1, 'Efectivo', -20.00),
(2, 'Transferencia', -20.00),
(3, 'Tarjeta de Débito', 0.00),
(4, 'Tarjeta de Crédito', 0.00);

-- 9. COMPRAS (3)
INSERT INTO compra (id_compra, fecha_compra, monto_total, id_proveedor) VALUES
(1, '2026-02-10 09:30:00', 450000.00, 1),
(2, '2026-02-20 11:00:00', 380000.00, 2),
(3, '2026-03-01 14:15:00', 210000.00, 3);

-- 10. DETALLE_COMPRA (8 renglones)
INSERT INTO detalle_compra (id_compra, renglon_compra, cantidad, precio_costo_unitario, id_variante) VALUES
(1, 1, 20, 8000.00, 1),
(1, 2, 10, 22000.00, 5),
(1, 3, 15, 6500.00, 3),
(2, 1, 5, 45000.00, 12),
(2, 2, 10, 15000.00, 17),
(2, 3, 10, 12000.00, 11),
(3, 1, 10, 28000.00, 15),
(3, 2, 20, 5000.00, 24);

-- 11. VENTAS (6 ventas) - Último día 2026-03-15 tiene 2 ventas (Consulta 3)
INSERT INTO venta (id_venta, fecha_hora, monto_total, id_medio_pago) VALUES
(1, '2026-03-02 10:15:00', 12800.00, 1),
(2, '2026-03-05 16:45:00', 56000.00, 4),
(3, '2026-03-08 11:20:00', 15000.00, 3),
(4, '2026-03-10 14:00:00', 44000.00, 4),
(5, '2026-03-15 09:30:00', 35200.00, 2),  -- Último día
(6, '2026-03-15 17:15:00', 10000.00, 3);  -- Último día

-- 12. DETALLE_VENTA (10 renglones)
INSERT INTO detalle_venta (id_venta, renglon_venta, cantidad, precio_unitario_cobrado, id_variante) VALUES
(1, 1, 1, 12800.00, 1),   -- Billetera Hombre Marrón
(2, 1, 1, 56000.00, 15),  -- Cartera Cuero Marrón
(3, 1, 1, 15000.00, 19),  -- Riñonera Negra
(4, 1, 1, 44000.00, 5),   -- Mochila Porta Notebook
(4, 2, 1, 10000.00, 24),  -- Vaso Térmico
(5, 1, 1, 35200.00, 5),   -- Mochila Porta Notebook (con desc)
(6, 1, 1, 10000.00, 24);  -- Vaso Térmico

-- 13. DEVOLUCIONES (3) - FK Compuesta (id_venta, renglon_venta)
-- Venta 1 renglon 1: cambio de variante 1 por variante 3
-- Venta 3 renglon 1: reparacion (id_variante_nueva es NULL)
-- Venta 4 renglon 1: devolucion directa (id_variante_nueva es NULL)
INSERT INTO devolucion (id_devolucion, fecha, id_venta, renglon_venta, cantidad, motivo, id_variante_nueva, monto_diferencia, observaciones) VALUES
(1, '2026-03-06 12:00:00', 1, 1, 1, 'CAMBIO', 3, -2400.00, 'Cambio Billetera Hombre por Dama'),
(2, '2026-03-11 17:30:00', 3, 1, 1, 'REPARACION', NULL, 0.00, 'Riñonera enviada a reparación de cierre'),
(3, '2026-03-12 11:00:00', 4, 1, 1, 'DEVOLUCION', NULL, 0.00, 'Devolución de Mochila por defecto en costura');

-- Ajuste de secuencias
SELECT setval(pg_get_serial_sequence('categoria', 'id_categoria'), (SELECT MAX(id_categoria) FROM categoria));
SELECT setval(pg_get_serial_sequence('material', 'id_material'), (SELECT MAX(id_material) FROM material));
SELECT setval(pg_get_serial_sequence('color', 'id_color'), (SELECT MAX(id_color) FROM color));
SELECT setval(pg_get_serial_sequence('tamano', 'id_tamano'), (SELECT MAX(id_tamano) FROM tamano));
SELECT setval(pg_get_serial_sequence('producto', 'id_producto'), (SELECT MAX(id_producto) FROM producto));
SELECT setval(pg_get_serial_sequence('variante_producto', 'id_variante'), (SELECT MAX(id_variante) FROM variante_producto));
SELECT setval(pg_get_serial_sequence('proveedor', 'id_proveedor'), (SELECT MAX(id_proveedor) FROM proveedor));
SELECT setval(pg_get_serial_sequence('medio_pago', 'id_medio_pago'), (SELECT MAX(id_medio_pago) FROM medio_pago));
SELECT setval(pg_get_serial_sequence('venta', 'id_venta'), (SELECT MAX(id_venta) FROM venta));
SELECT setval(pg_get_serial_sequence('compra', 'id_compra'), (SELECT MAX(id_compra) FROM compra));
SELECT setval(pg_get_serial_sequence('devolucion', 'id_devolucion'), (SELECT MAX(id_devolucion) FROM devolucion));
