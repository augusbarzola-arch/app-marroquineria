
-- DML - POBLADO DE DATOS


-- CATEGORIAS
INSERT INTO categoria (id_categoria, nombre_categoria, descripcion) VALUES
(1, 'Billeteras', 'Billeteras y tarjeteros de dama y hombre'),
(2, 'Mochilas y Monomochilas', 'Mochilas urbanas, ejecutivas e infantiles'),
(3, 'Valijas y Viaje', 'Valijas rígidas, blandas y bolsos de viaje'),
(4, 'Carteras y Bolsos', 'Carteras de mano, bandoleras y bolsos deportivos'),
(5, 'Riñoneras y Portafolios', 'Riñoneras para dama/hombre y portafolios de trabajo'),
(6, 'Electrónica y Accesorios', 'Accesorios complementarios, vasos térmicos y gadgets');

-- MATERIALES
INSERT INTO material (id_material, nombre_material) VALUES
(1, 'Cuero Vacuno'),
(2, 'Cuero Sintético / PU'),
(3, 'Lona / Cordura'),
(4, 'Poliéster / Nylon'),
(5, 'Acero Inoxidable');

-- COLORES
INSERT INTO color (id_color, nombre_color) VALUES
(1, 'Negro'),
(2, 'Azul'),
(3, 'Rojo'),
(4, 'Marrón'),
(5, 'Beige'),
(6, 'Único');

-- TAMAÑOS
INSERT INTO tamano (id_tamano, nombre_tamano) VALUES
(1, 'Grande'),
(2, 'Chica'),
(3, 'Mediano'),
(4, 'Único');

-- PRODUCTOS
INSERT INTO producto (id_producto, nombre_producto, descripcion, precio_costo, precio_lista, id_categoria, id_material) VALUES
(1, 'Billetera Hombre Clásica', 'Billetera con tarjetero y billetero', 8000.00, 16000.00, 1, 1),
(2, 'Billetera Dama Cierre Cuerina', 'Billetera espaciosa con cierre perimetral', 6500.00, 13000.00, 1, 2),
(3, 'Mochila Urbana Porta Notebook', 'Mochila reforzada acolchada para laptop 15.6 pulgadas', 22000.00, 44000.00, 2, 4),
(4, 'Monomochila Infantil', 'Monomochila pequeña cruzada para niños', 9000.00, 18000.00, 2, 3),
(5, 'Valija 24 Rígida Carry On', 'Valija de cabina 4 ruedas 360 grados', 45000.00, 90000.00, 3, 2),
(6, 'Cartera Bandolera de Cuero', 'Cartera de hombro con apliques metálicos', 28000.00, 56000.00, 4, 1),
(7, 'Bolso Deportivo 50L', 'Bolso amplio para gimnasio o viaje corto', 15000.00, 30000.00, 4, 3),
(8, 'Riñonera Urbana Unisex', 'Riñonera con triple compartimento', 7500.00, 15000.00, 5, 4),
(9, 'Vaso Térmico 500ml', 'Vaso de acero inoxidable frío/calor', 5000.00, 10000.00, 6, 5);

-- VARIANTES DE PRODUCTO
INSERT INTO variante_producto (id_variante, id_producto, id_color, id_tamano, stock_actual, stock_minimo) VALUES
(1, 1, 4, 4, 25, 5),   -- Billetera Hombre Marrón Único
(2, 2, 5, 4, 18, 5),   -- Billetera Dama Beige Único
(3, 3, 1, 4, 4, 1),    -- Mochila Urbana Negra Único
(4, 3, 2, 4, 2, 1),    -- Mochila Urbana Azul Único
(5, 3, 3, 4, 3, 1),    -- Mochila Urbana Roja Único
(6, 4, 6, 4, 15, 4),   -- Monomochila Único
(7, 5, 1, 1, 2, 1),    -- Valija Negra Grande
(8, 5, 1, 2, 1, 1),    -- Valija Negra Chica
(9, 6, 4, 4, 10, 3),   -- Cartera Marrón Único
(10, 7, 1, 4, 14, 4),  -- Bolso Deportivo Negro Único
(11, 8, 1, 4, 12, 5),  -- Riñonera Negra Único
(12, 8, 2, 4, 8, 5),   -- Riñonera Azul Único
(13, 9, 6, 4, 30, 8);  -- Vaso Térmico Único

-- PROVEEDORES
INSERT INTO proveedor (id_proveedor, cuit, razon_social, telefono, email) VALUES
(1, '30-71123456-8', 'Taller Marroquí S.A.', '1140001111', 'ventas@tallermarroqui.com'),
(2, '30-68987654-2', 'Importadora BagStyle SRL', '1142223333', 'contacto@bagstyle.com'),
(3, '30-54321876-5', 'Distribuidora del Cuero Argentina', '1144445555', 'pedidos@distdelcuero.com');

-- MEDIOS DE PAGO
INSERT INTO medio_pago (id_medio_pago, nombre_medio, porcentaje_descuento_recargo) VALUES
(1, 'Efectivo', -20.00),
(2, 'Transferencia', -20.00),
(3, 'Tarjeta de Débito', 0.00),
(4, 'Tarjeta de Crédito', 0.00);

-- VENTAS
INSERT INTO venta (id_venta, fecha_hora, monto_total, id_medio_pago) VALUES
(1, '2026-03-01 10:15:00', 12800.00, 1),
(2, '2026-03-01 16:45:00', 56000.00, 4),
(3, '2026-03-02 11:20:00', 15000.00, 3);

-- DETALLE_VENTA
INSERT INTO detalle_venta (id_venta, renglon_venta, cantidad, precio_unitario_cobrado, id_variante) VALUES
(1, 1, 1, 12800.00, 1),
(2, 1, 1, 56000.00, 9),
(3, 1, 1, 15000.00, 11);

-- COMPRAS
INSERT INTO compra (id_compra, fecha_compra, monto_total, id_proveedor) VALUES
(1, '2026-02-10 09:30:00', 360000.00, 1),
(2, '2026-02-20 11:00:00', 355000.00, 2);

-- DETALLE_COMPRA
INSERT INTO detalle_compra (id_compra, renglon_compra, cantidad, precio_costo_unitario, id_variante) VALUES
(1, 1, 20, 8000.00, 1),
(1, 2, 10, 20000.00, 3),
(2, 1, 5, 45000.00, 7),
(2, 2, 10, 13000.00, 10);

-- DEVOLUCIONES
INSERT INTO devolucion (id_devolucion, fecha, id_venta, id_variante_devuelta, cantidad, motivo, id_variante_nueva, monto_diferencia, observaciones) VALUES
(1, '2026-03-05 12:00:00', 1, 1, 1, 'CAMBIO', 2, -2400.00, 'Cambio Billetera Hombre por Dama'),
(2, '2026-03-06 17:30:00', 3, 11, 1, 'REPARACION', NULL, 0.00, 'Riñonera enviada a reparación de cierre');

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