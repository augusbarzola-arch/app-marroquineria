
-- DDL - CREACIÓN DE TABLAS


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

-- 4. TAMAÑO
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

-- 10. DETALLE_VENTA
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

-- 12. DETALLE_COMPRA
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
    id_venta INT NOT NULL REFERENCES venta(id_venta),
    id_variante_devuelta INT NOT NULL REFERENCES variante_producto(id_variante),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    motivo VARCHAR(20) NOT NULL CHECK (motivo IN ('CAMBIO','REPARACION','DEVOLUCION')),
    id_variante_nueva INT REFERENCES variante_producto(id_variante),
    monto_diferencia DECIMAL(10,2) DEFAULT 0,
    observaciones VARCHAR(255)
);