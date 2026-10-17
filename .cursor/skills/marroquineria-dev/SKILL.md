---
name: marroquineria-dev
description: Flujo de trabajo para el proyecto de marroquinería. Usar cuando se necesite modificar código, agregar features o corregir bugs en esta app.
---

# Protocolo de Trabajo - Proyecto Marroquinería

## Contexto del Proyecto

Aplicación web para gestionar una marroquinería. Stack: **Python + FastAPI + PostgreSQL + Jinja2 + Bootstrap 5**. La app ya está en funcionamiento y conectada a la base de datos `marroquineria`.

## Estructura de Referencia

- **`docs/ddl_tif.sql`**: Definición exacta de las 13 tablas. LEER antes de tocar código.
- **`docs/dml-poblado_tif.sql`**: Datos de prueba cargados.
- **`docs/consultas_tif.sql`**: Consultas de ejemplo que la app debe resolver.
- **`app/`**: Código fuente completo.
- **`app/routers/`**: Endpoints de FastAPI.
- **`app/templates/`**: Plantillas Jinja2 (HTML).
- **`app/services/`**: Lógica de negocio (transacciones, stock).

## Reglas de Negocio Inmutables

1. No hay tablas de cliente, empleado, ni facturación.
2. El stock se actualiza automáticamente en ventas, compras y devoluciones.
3. Los descuentos/recargos están en `medio_pago.porcentaje_descuento_recargo` (negativo = descuento, positivo = recargo).
4. `motivo` en `devolucion` solo acepta: `'CAMBIO'`, `'REPARACION'`, `'DEVOLUCION'`.
5. Usar `tamano` (sin ñ) para la tabla de talles.

## Protocolo de Trabajo por Fases

Seguir SIEMPRE este orden para cualquier tarea:

### Fase 0: Descubrimiento
- Leer los archivos relevantes de `docs/` y el código actual antes de proponer cambios.
- NO asumir nada. Si hay dudas, preguntar.

### Fase 1: Planificación
- Mostrar un **plan de acción numerado** con los pasos propuestos.
- **Esperar confirmación explícita del usuario** ("ok", "dale", "confirmado") antes de escribir código.
- NUNCA pasar a la Fase 2 sin esa confirmación.

### Fase 2: Ejecución
- Escribir el código según el plan aprobado.
- Usar **transacciones atómicas** en operaciones multi-tabla.
- Comentar el código en español en las partes clave.
- No modificar archivos que no estén relacionados con la tarea.

### Fase 3: Verificación
- Mostrar **cómo se verificó** que el cambio funciona (captura de log, salida de terminal, etc.).
- Si algo falla, explicar el error y proponer una solución.

## Tareas Pendientes (actualizado)

Estas son las tareas que el usuario pidió y que deben resolverse en orden:

1. **Bug: Caracteres con tilde se ven mal** → Revisar `<meta charset="UTF-8">` en templates.
2. **Bug: Filtro de productos se rompe** → Revisar endpoint y llamada AJAX.
3. **Feature: Agregar campo SKU a productos** → Migración SQL + modelo + formulario + vista.
4. **Bug: Filtro de stock/variantes se rompe** → Error 422 en logs, revisar parámetros.
5. **Feature: Módulo de Reportes no funciona** → Implementar los 7 reportes con CSV y PDF.
6. **UX/UI: Rediseño completo** → Dark mode, glassmorphism, tipografía moderna (Inter/Poppins).
7. **UX: Historial de ventas feo** → Rediseñar tabla con columnas claras.
8. **Explicación: ¿Para qué sirve el POS?** → Documentar brevemente.

## Lo que NO hacer

- No agregar login/usuarios/autenticación.
- No agregar facturación electrónica ni AFIP.
- No usar ORM (SQL directo con psycopg2).
- No modificar la estructura de las tablas sin autorización.
- No instalar nuevas dependencias sin preguntar.