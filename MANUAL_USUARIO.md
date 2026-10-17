# Manual de Usuario - Sistema de Marroquinería

¡Bienvenido/a al sistema de gestión de la marroquinería! Este manual está diseñado para que cualquier persona del equipo, sin importar sus conocimientos técnicos, pueda utilizar el sistema en el día a día para registrar ventas, controlar el stock, recibir mercadería y atender devoluciones de clientes.

---

## 1. ¿Cómo Ingresar al Sistema?

1. Encienda la computadora y abra su navegador web de preferencia (Google Chrome, Microsoft Edge o Mozilla Firefox).
2. En la barra de direcciones de arriba escriba:
   ```text
   http://localhost:8000
   ```
3. Presione **Enter**. Inmediatamente verá el **Panel de Control (Dashboard)** del negocio.

> [!TIP]
> **Modo Oscuro / Modo Claro:** Arriba a la derecha encontrará el botón con icono de luna/sol para alternar entre el tema claro y oscuro según su comodidad visual.
>
> **Atajo rápido:** Puede presionar la tecla **`F2`** en su teclado en cualquier momento para ir directamente a la pantalla de venta.

---

## 2. Pantalla de Inicio (Dashboard)

El Dashboard le muestra de un vistazo la salud comercial del negocio:
- **Ventas de Hoy:** Dinero total cobrado en el día y cantidad de ventas hechas.
- **Ventas del Mes:** Facturación acumulada en el mes en curso.
- **Ticket Promedio:** Cuánto gasta un cliente en promedio por cada compra.
- **Variantes en Stock Bajo (en rojo):** Cantidad de artículos que se están agotando.
- **Gráfico de Líneas:** Muestra la curva de ventas de los últimos 30 días para evaluar si las ventas están subiendo o bajando.
- **Tabla de Alerta Roja:** Lista los productos específicos que llegaron al stock mínimo para que sepa qué tiene que reponer o encargar al proveedor de inmediato.

---

## 3. Cómo Hacer una Venta en el Mostrador (Punto de Venta - POS)

Para cobrarle a un cliente, presione la tecla **`F2`** o haga clic en **"Punto de Venta (POS)"** en el menú de la izquierda. La pantalla se divide en tres partes:

### Paso 1: Buscar los artículos (Panel Izquierdo)
1. En el buscador escriba parte del nombre del producto (por ejemplo, `mochila` o `billetera`), o seleccione la categoría.
2. Cada producto muestra sus variantes disponibles con su color, talle y stock disponible.
3. Haga clic sobre el botón de la variante que el cliente se lleva para sumarla al carrito.

### Paso 2: Revisar el Carrito (Panel Central)
- En el centro verá los productos elegidos.
- Puede subir o bajar la cantidad con los botones **`+`** y **`-`**. El sistema no le permitirá vender más unidades de las que realmente hay en el local.
- Si se equivocó de producto, presione el botón rojo con la cruz (**`x`**) para quitarlo.

### Paso 3: Elegir el Medio de Pago y Cobrar (Panel Derecho)
1. Seleccione cómo abona el cliente:
   - **Efectivo o Transferencia:** Aplica automáticamente un **20% de descuento** sobre el precio de lista.
   - **Tarjeta de Débito o Crédito:** Mantiene el precio de lista sin recargos.
2. Observe el desglose en pantalla: verá el subtotal, el descuento aplicado y el **Total Final**.
3. Haga clic en el botón verde grande **"Confirmar Venta"**.

### Paso 4: Comprobante Interno
- Al confirmar, el sistema descuenta automáticamente las unidades del stock y abre el **Comprobante Interno**.
- Haga clic en **"Imprimir Comprobante"** para imprimir el ticket en papel para el cliente.
- Presione **`F2`** para quedar listo/a para la próxima venta.

---

## 4. Cómo Gestionar un Cambio, Reparación o Devolución

Cuando un cliente regresa al local con un producto, vaya a **"Devoluciones"** en el menú y haga clic en **"Nueva Devolución / Cambio"**:

1. **Buscar la Venta Original:** Ingrese el número de ticket que trajo el cliente (por ejemplo: `1`) y haga clic en **"Cargar Venta"**.
2. **Elegir el Artículo:** El sistema listará lo que el cliente compró en esa venta, cuántas unidades llevó y cuántas ya devolvió. Seleccione el artículo que el cliente entrega en el mostrador.
3. **Indicar la Cantidad:** Escriba cuántas unidades devuelve (no puede devolver más de las que compró).
4. **Seleccionar el Motivo:**
   - **CAMBIO (por otro producto):** 
     - Se abrirá un menú para elegir la nueva variante que se lleva el cliente.
     - El sistema calcula solo si hay diferencia económica:
       - Si la nueva prenda es más cara: le indica cuánto dinero debe poner el cliente arriba.
       - Si es más barata: le indica cuánto dinero tiene a favor el cliente.
     - El sistema sumará al stock la prenda que devuelve y restará la prenda nueva que se lleva.
   - **DEVOLUCIÓN (el cliente no quiere el producto):** 
     - Se reintegra el dinero al cliente y el sistema vuelve a sumar el producto al stock del local.
   - **REPARACIÓN (se manda al taller por cierre, costura o falla):** 
     - Queda asentado el problema en el sistema, pero el stock no se altera.
5. Ingrese observaciones si desea (ej: *"falla en el cierre del bolsillo delantero"*) y presione **"Confirmar Operación"**.

---

## 5. Cómo Recibir Mercadería de un Proveedor (Compras)

Cuando el camión o taller entrega un pedido de mercadería:

1. Vaya a **"Compras"** y luego a **"Nueva Orden de Compra"**.
2. **Seleccione el Proveedor** que le entregó el pedido.
3. **Cargar los Artículos Recibidos:**
   - Elija el producto, color y talle en el desplegable.
   - El sistema traerá automáticamente el costo de referencia. Puede modificar el costo unitario si el proveedor le cambió el precio.
   - Ingrese la cantidad de unidades que entraron en la caja.
   - Presione **"Agregar"**.
4. Repita para todos los artículos que vinieron en el envío.
5. Compruebe que el **Total Compra** coincida con el remito o factura del proveedor.
6. Haga clic en **"Confirmar Compra y Sumar Stock"**.
7. En ese instante, todas las unidades ingresadas se **suman automáticamente al inventario del negocio**.

---

## 6. Control y Corrección Rápida de Stock

Si hace un recuento físico en el local o depósito y nota diferencias:

1. Ingrese a **"Stock / Variantes"** en el menú izquierdo.
2. Puede usar los filtros arriba para ver solo una categoría, un color, o activar la casilla **"Solo Stock Bajo"**.
3. En la misma tabla, las celdas de **Stock Actual** y **Stock Mínimo** son cajas editables:
   - Modifique el número directamente con su teclado.
   - Presione el botón verde con tilde (**✓**) al final de la fila (o presione **Enter**).
4. El cambio se guarda al instante y la fila cambiará de color sola si el stock quedó en nivel normal (verde), cercano al límite (amarillo) o en falta (rojo).

---

## 7. Alta de Nuevos Productos y Variantes

Cuando comience a fabricar o vender un modelo nuevo:

1. Vaya a **"Productos"** y presione **"Nuevo Producto"**.
2. Complete el nombre, descripción, elija la categoría y el material.
3. Ingrese el **Precio de Costo** y el **Precio de Lista** de venta al público.
   - *Nota:* Si por error ingresa un precio de venta menor al costo, una alerta amarilla le avisará para evitar pérdidas.
4. Presione **"Crear Producto"**.
5. En la ficha que se abrirá a continuación, presione **"Agregar Variante"** para dar de alta las combinaciones de color y talle en que se fabrica ese modelo (ej: Negro Grande, Marrón Único), indicando con cuántas unidades arranca.

---

## 8. Consulta y Exportación de Reportes

Para presentarle informes al dueño, contador o administración:

1. Ingrese a **"Reportes"** en el menú.
2. Elija la pestaña del informe que necesita:
   - **Ventas por Fecha:** Cuánto se facturó día por día y el ticket promedio.
   - **Top 10 Productos:** Los artículos más vendidos y que más dinero recaudaron.
   - **Por Medio de Pago:** Cuánto ingresó en efectivo, transferencia o tarjetas.
   - **Compras por Proveedor:** A quién se le compró más mercadería.
   - **Devoluciones:** Cantidad de cambios y reparaciones efectuadas.
   - **Stock Valorizado:** Valor total en dinero de todo lo que hay guardado en el depósito y mostrador al costo.
   - **Stock Bajo:** Listado completo de faltantes para hacer pedidos.
3. Si lo desea, elija el rango de fechas (*Desde / Hasta*) y haga clic en **"Aplicar Filtro"**.
4. Haga clic en:
   - **"Exportar CSV"** para abrir los datos en una planilla de **Microsoft Excel**.
   - **"Exportar PDF"** para generar un documento formal listo para imprimir o enviar por correo electrónico.

---

## 9. Resumen de Teclas y Consejos Útiles

| Tecla | Función |
| :--- | :--- |
| **`F2`** | Abre inmediatamente la pantalla de Nueva Venta en cualquier momento. |
| **`ESC`** | Cierra cualquier ventana o modal que tenga abierta en pantalla. |
| **`Enter`** | En el buscador del POS, agrega automáticamente el primer producto con stock. |

- **Si un producto no tiene color o talle específico:** Seleccione siempre la opción llamada **"Único"**.
- **Para salir de dudas:** Revise el historial de ventas o el stock valorizado; todas las operaciones quedan registradas de forma permanente y segura en el sistema.
