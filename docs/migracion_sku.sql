-- MIGRACIÓN: AGREGAR CAMPO SKU A TABLA PRODUCTO
\encoding UTF8
SET client_encoding = 'UTF8';

BEGIN;

ALTER TABLE producto ADD COLUMN IF NOT EXISTS sku VARCHAR(30) UNIQUE;

UPDATE producto 
SET sku = 'PROD-' || LPAD(id_producto::text, 3, '0')
WHERE sku IS NULL;

COMMIT;
