-- ============================================================================
-- SCRIPT DE INICIALIZACIÓN COMPLETA PARA SUPABASE
-- Sistema de Gestión y Tienda Web de Marroquinería
-- ============================================================================
SET client_encoding = 'UTF8';

-- PARTE 1: TABLAS BASE, TRIGGERS Y FUNCIONES EN PL/PGSQL

-- DDL - CREACIÓN DE TABLAS
-- Sistema de Gestión Comercial - Marroquinería


DROP TABLE IF EXISTS devolucion CASCADE;
DROP TABLE IF EXISTS detalle_venta CASCADE;
DROP TABLE IF EXISTS detalle_compra CASCADE;
DROP TABLE IF EXISTS venta CASCADE;
DROP TABLE IF EXISTS compra CASCADE;
DROP TABLE IF EXISTS variante_producto CASCADE;
DROP TABLE IF EXISTS producto CASCADE;
DROP TABLE IF EXISTS color CASCADE;
DROP TABLE IF EXISTS tamano CASCADE;
DROP TABLE IF EXISTS categoria CASCADE;
DROP TABLE IF EXISTS material CASCADE;
DROP TABLE IF EXISTS proveedor CASCADE;
DROP TABLE IF EXISTS medio_pago CASCADE;

-- 1. CATEGORIA
CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

-- 2. MATERIAL
CREATE TABLE material (
    id_material SERIAL PRIMARY KEY,
    nombre_material VARCHAR(50) NOT NULL
);

-- 3. COLOR
CREATE TABLE color (
    id_color SERIAL PRIMARY KEY,
    nombre_color VARCHAR(30) NOT NULL UNIQUE
);

-- 4. TAMANO (sin ñ, unificado en todo el proyecto)
CREATE TABLE tamano (
    id_tamano SERIAL PRIMARY KEY,
    nombre_tamano VARCHAR(20) NOT NULL UNIQUE
);

-- 5. PRODUCTO
CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    nombre_producto VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio_costo DECIMAL(10,2) NOT NULL CHECK (precio_costo >= 0),
    precio_lista DECIMAL(10,2) NOT NULL CHECK (precio_lista >= 0),
    id_categoria INT NOT NULL REFERENCES categoria(id_categoria),
    id_material INT NOT NULL REFERENCES material(id_material)
);

-- 6. VARIANTE_PRODUCTO
CREATE TABLE variante_producto (
    id_variante SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES producto(id_producto) ON DELETE CASCADE,
    id_color INT NOT NULL REFERENCES color(id_color),
    id_tamano INT NOT NULL REFERENCES tamano(id_tamano),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    CONSTRAINT uq_variante_producto UNIQUE (id_producto, id_color, id_tamano)
);

-- 7. PROVEEDOR
CREATE TABLE proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    cuit VARCHAR(20) NOT NULL UNIQUE,
    razon_social VARCHAR(100) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(100)
);

-- 8. MEDIO_PAGO
CREATE TABLE medio_pago (
    id_medio_pago SERIAL PRIMARY KEY,
    nombre_medio VARCHAR(50) NOT NULL,
    porcentaje_descuento_recargo DECIMAL(5,2) NOT NULL DEFAULT 0.00
        CHECK (porcentaje_descuento_recargo BETWEEN -100 AND 100)
);

-- 9. VENTA
CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto_total DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (monto_total >= 0),
    id_medio_pago INT NOT NULL REFERENCES medio_pago(id_medio_pago)
);

-- 10. DETALLE_VENTA (entidad débil)
CREATE TABLE detalle_venta (
    id_venta INT NOT NULL REFERENCES venta(id_venta) ON DELETE CASCADE,
    renglon_venta INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario_cobrado DECIMAL(10,2) NOT NULL CHECK (precio_unitario_cobrado >= 0),
    id_variante INT NOT NULL REFERENCES variante_producto(id_variante),
    PRIMARY KEY (id_venta, renglon_venta)
);

-- 11. COMPRA
CREATE TABLE compra (
    id_compra SERIAL PRIMARY KEY,
    fecha_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto_total DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (monto_total >= 0),
    id_proveedor INT NOT NULL REFERENCES proveedor(id_proveedor)
);

-- 12. DETALLE_COMPRA (entidad débil)
CREATE TABLE detalle_compra (
    id_compra INT NOT NULL REFERENCES compra(id_compra) ON DELETE CASCADE,
    renglon_compra INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_costo_unitario DECIMAL(10,2) NOT NULL CHECK (precio_costo_unitario >= 0),
    id_variante INT NOT NULL REFERENCES variante_producto(id_variante),
    PRIMARY KEY (id_compra, renglon_compra)
);

-- 13. DEVOLUCION
CREATE TABLE devolucion (
    id_devolucion SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_venta INT NOT NULL,
    renglon_venta INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    motivo VARCHAR(20) NOT NULL CHECK (motivo IN ('CAMBIO','REPARACION','DEVOLUCION')),
    id_variante_nueva INT REFERENCES variante_producto(id_variante),
    monto_diferencia DECIMAL(10,2) DEFAULT 0,
    observaciones VARCHAR(255),
    -- FK compuesta: garantiza que la devolución sea de un ítem de esa venta
    FOREIGN KEY (id_venta, renglon_venta)
        REFERENCES detalle_venta(id_venta, renglon_venta)
        ON DELETE CASCADE,
    -- CHECK: si es CAMBIO debe haber variante nueva; si no, no debe haber
    CONSTRAINT chk_cambio CHECK ((motivo = 'CAMBIO') = (id_variante_nueva IS NOT NULL))
);

-- ============================================================
-- TRIGGERS PARA MANTENER EL STOCK AUTOMÁTICAMENTE
-- ============================================================

-- VENTA: al insertar renglón, descuenta stock
CREATE OR REPLACE FUNCTION fn_venta_stock_ins() RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
       SET stock_actual = stock_actual - NEW.cantidad
     WHERE id_variante = NEW.id_variante;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_venta_stock_ins
AFTER INSERT ON detalle_venta
FOR EACH ROW EXECUTE FUNCTION fn_venta_stock_ins();

-- VENTA: al eliminar renglón, devuelve stock
CREATE OR REPLACE FUNCTION fn_venta_stock_del() RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
       SET stock_actual = stock_actual + OLD.cantidad
     WHERE id_variante = OLD.id_variante;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_venta_stock_del
AFTER DELETE ON detalle_venta
FOR EACH ROW EXECUTE FUNCTION fn_venta_stock_del();

-- COMPRA: al insertar renglón, suma stock
CREATE OR REPLACE FUNCTION fn_compra_stock_ins() RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
       SET stock_actual = stock_actual + NEW.cantidad
     WHERE id_variante = NEW.id_variante;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compra_stock_ins
AFTER INSERT ON detalle_compra
FOR EACH ROW EXECUTE FUNCTION fn_compra_stock_ins();

-- COMPRA: al eliminar renglón, descuenta stock
CREATE OR REPLACE FUNCTION fn_compra_stock_del() RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
       SET stock_actual = stock_actual - OLD.cantidad
     WHERE id_variante = OLD.id_variante;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compra_stock_del
AFTER DELETE ON detalle_compra
FOR EACH ROW EXECUTE FUNCTION fn_compra_stock_del();

-- DEVOLUCION: al insertar, ajusta stock según el motivo
--   DEVOLUCION: +cantidad al stock de la variante original
--   CAMBIO:     +cantidad a la variante original y -cantidad a la variante nueva
--   REPARACION: sin cambio (el ítem vuelve al local luego de repararse)
CREATE OR REPLACE FUNCTION fn_devolucion_stock_ins() RETURNS TRIGGER AS $$
DECLARE
    v_variante_original INT;
BEGIN
    -- Obtener la variante original desde el renglón de venta
    SELECT id_variante
      INTO v_variante_original
      FROM detalle_venta
     WHERE id_venta = NEW.id_venta
       AND renglon_venta = NEW.renglon_venta;

    IF NEW.motivo = 'DEVOLUCION' THEN
        UPDATE variante_producto
           SET stock_actual = stock_actual + NEW.cantidad
         WHERE id_variante = v_variante_original;

    ELSIF NEW.motivo = 'CAMBIO' THEN
        -- El ítem devuelto vuelve al stock
        UPDATE variante_producto
           SET stock_actual = stock_actual + NEW.cantidad
         WHERE id_variante = v_variante_original;
        -- El ítem nuevo sale del stock
        UPDATE variante_producto
           SET stock_actual = stock_actual - NEW.cantidad
         WHERE id_variante = NEW.id_variante_nueva;
    END IF;
    -- REPARACION: no modifica stock

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_devolucion_stock_ins
AFTER INSERT ON devolucion
FOR EACH ROW EXECUTE FUNCTION fn_devolucion_stock_ins();

-- PARTE 2: MÓDULO DE E-COMMERCE (IMÁGENES, PEDIDOS WEB, WEBHOOKS)
-- MIGRACIÓN DDL: MÓDULO DE E-COMMERCE INTEGRADO
SET client_encoding = 'UTF8';

BEGIN;

-- 1. Tabla de Imágenes de Productos
CREATE TABLE IF NOT EXISTS producto_imagen (
    id_imagen SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES producto(id_producto) ON DELETE CASCADE,
    url_imagen VARCHAR(500) NOT NULL,
    es_portada BOOLEAN DEFAULT FALSE,
    orden INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_producto_imagen_producto ON producto_imagen(id_producto);

-- 2. Tabla de Pedidos / Órdenes Web
CREATE TABLE IF NOT EXISTS pedido_web (
    id_pedido SERIAL PRIMARY KEY,
    codigo_seguimiento VARCHAR(30) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nombre_cliente VARCHAR(100) NOT NULL,
    email_cliente VARCHAR(120) NOT NULL,
    telefono_cliente VARCHAR(30) NOT NULL,
    direccion_envio VARCHAR(200) NOT NULL,
    zona_envio VARCHAR(50) NOT NULL,
    costo_envio DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (costo_envio >= 0),
    metodo_pago VARCHAR(30) NOT NULL CHECK (metodo_pago IN ('TRANSFERENCIA', 'MERCADOPAGO')),
    estado VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE_PAGO' CHECK (estado IN ('PENDIENTE_PAGO', 'PAGADO', 'ENVIADO', 'CANCELADO')),
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (subtotal >= 0),
    total DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (total >= 0),
    comprobante_url VARCHAR(500),
    mp_preference_id VARCHAR(120),
    mp_payment_id VARCHAR(120),
    fecha_expiracion TIMESTAMP,
    observaciones TEXT
);

CREATE INDEX IF NOT EXISTS idx_pedido_web_estado ON pedido_web(estado);
CREATE INDEX IF NOT EXISTS idx_pedido_web_fecha ON pedido_web(fecha_creacion DESC);
CREATE INDEX IF NOT EXISTS idx_pedido_web_codigo ON pedido_web(codigo_seguimiento);

-- 3. Tabla de Detalle de Ítems del Pedido Web
CREATE TABLE IF NOT EXISTS detalle_pedido_web (
    id_pedido INT NOT NULL REFERENCES pedido_web(id_pedido) ON DELETE CASCADE,
    renglon INT NOT NULL,
    id_variante INT NOT NULL REFERENCES variante_producto(id_variante),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario_cobrado DECIMAL(10,2) NOT NULL CHECK (precio_unitario_cobrado >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    PRIMARY KEY (id_pedido, renglon)
);

CREATE INDEX IF NOT EXISTS idx_detalle_pedido_web_variante ON detalle_pedido_web(id_variante);

-- 4. Registro de Webhooks de Mercado Pago (Garantía de Idempotencia)
CREATE TABLE IF NOT EXISTS mp_webhook_log (
    id_evento VARCHAR(120) PRIMARY KEY,
    tipo_evento VARCHAR(50),
    fecha_recepcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    procesado BOOLEAN DEFAULT TRUE,
    payload JSONB
);

COMMIT;


-- PARTE 3: POBLADO DE DATOS BASE Y VARIANTES
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


-- ============================================================================
-- SEGURIDAD SUPABASE (LINTER Y ASESOR DE SEGURIDAD)
-- ============================================================================
-- 1. Habilitar Row Level Security (RLS) en todas las tablas públicas
ALTER TABLE public.producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.detalle_venta ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.venta ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.variante_producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.color ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tamano ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categoria ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.devolucion ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.detalle_compra ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.compra ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.proveedor ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.producto_imagen ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pedido_web ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mp_webhook_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.material ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.medio_pago ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.detalle_pedido_web ENABLE ROW LEVEL SECURITY;

-- 2. Fijar search_path inmutable para funciones PL/pgSQL
ALTER FUNCTION public.fn_venta_stock_ins() SET search_path = public;
ALTER FUNCTION public.fn_venta_stock_del() SET search_path = public;
ALTER FUNCTION public.fn_compra_stock_ins() SET search_path = public;
ALTER FUNCTION public.fn_compra_stock_del() SET search_path = public;
ALTER FUNCTION public.fn_devolucion_stock_ins() SET search_path = public;
