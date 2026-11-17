
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