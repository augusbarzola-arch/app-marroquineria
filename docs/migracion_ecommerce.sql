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
