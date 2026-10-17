-- REPARACIÓN DE TILDES Y MOJIBAKE EN POSTGRESQL
\encoding UTF8
SET client_encoding = 'UTF8';
BEGIN;
UPDATE categoria SET descripcion = 'Valijas rígidas, blandas y bolsos de viaje' WHERE id_categoria = 3;
UPDATE material SET nombre_material = 'Cuero Sintético / PU' WHERE id_material = 2;
UPDATE material SET nombre_material = 'Poliéster / Nylon' WHERE id_material = 4;
UPDATE color SET nombre_color = 'Marrón' WHERE id_color = 4;
UPDATE color SET nombre_color = 'Único' WHERE id_color = 6;
UPDATE tamano SET nombre_tamano = 'Único' WHERE id_tamano = 4;
UPDATE proveedor SET razon_social = 'Taller Marroquí S.A.' WHERE id_proveedor = 1;
UPDATE producto SET nombre_producto = 'Billetera Hombre Clásica' WHERE id_producto = 1;
UPDATE producto SET descripcion = 'Monomochila pequeña cruzada para niños' WHERE id_producto = 4;
UPDATE producto SET nombre_producto = 'Valija 24 Rígida Carry On' WHERE id_producto = 5;
UPDATE producto SET descripcion = 'Cartera de hombro con apliques metálicos' WHERE id_producto = 6;
UPDATE producto SET nombre_producto = 'Riñonera Urbana Unisex', descripcion = 'Riñonera con triple compartimento' WHERE id_producto = 8;
UPDATE producto SET nombre_producto = 'Vaso Térmico 500ml', descripcion = 'Vaso de acero inoxidable frío/calor' WHERE id_producto = 9;
COMMIT;
