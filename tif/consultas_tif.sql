-- Stock por producto y color
SELECT p.nombre_producto, c.nombre_color, t.nombre_tamano, v.stock_actual, v.stock_minimo
FROM variante_producto v
JOIN producto p ON p.id_producto = v.id_producto
JOIN color c ON c.id_color = v.id_color
JOIN tamano t ON t.id_tamano = v.id_tamano
ORDER BY p.nombre_producto, c.nombre_color;

-- Variantes con stock por debajo del mínimo
SELECT p.nombre_producto, c.nombre_color, t.nombre_tamano, v.stock_actual, v.stock_minimo
FROM variante_producto v
JOIN producto p ON p.id_producto = v.id_producto
JOIN color c ON c.id_color = v.id_color
JOIN tamano t ON t.id_tamano = v.id_tamano
WHERE v.stock_actual <= v.stock_minimo;

-- Ventas del día con medio de pago
SELECT v.id_venta, v.fecha_hora, mp.nombre_medio, v.monto_total
FROM venta v
JOIN medio_pago mp ON mp.id_medio_pago = v.id_medio_pago
WHERE DATE(v.fecha_hora) = '2026-03-01';

-- Devoluciones del mes
SELECT d.id_devolucion, d.fecha, d.motivo, p.nombre_producto, c.nombre_color, d.cantidad
FROM devolucion d
JOIN variante_producto v ON v.id_variante = d.id_variante_devuelta
JOIN producto p ON p.id_producto = v.id_producto
JOIN color c ON c.id_color = v.id_color
WHERE DATE_TRUNC('month', d.fecha) = DATE_TRUNC('month', CURRENT_DATE);