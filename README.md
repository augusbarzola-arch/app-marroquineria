# Sistema de Gestión para Marroquinería

Aplicación web integral para la administración y gestión comercial de una marroquinería (fábrica y venta de artículos de cuero), diseñada para operar de forma local en la PC del negocio mediante navegador web.

El sistema cubre la totalidad de las operaciones del negocio: catálogo de artículos, control de stock por variante de color y talle, punto de venta (POS) interactivo en tiempo real con descuento transaccional, registro de compras a proveedores con incremento de inventario, gestión post-venta de cambios, reparaciones y devoluciones, y reportes analíticos con exportación a **CSV** y **PDF**.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.11+
- **Backend Framework:** FastAPI 0.115.6
- **Servidor ASGI:** Uvicorn 0.34.0
- **Base de Datos:** PostgreSQL 14+
- **Driver de Base de Datos:** `psycopg2-binary` (pool multihilo `ThreadedConnectionPool`)
- **Acceso a Datos:** **SQL directo sin ORM**, manteniendo consultas nativas parametrizadas para prevenir inyección SQL.
- **Motor de Plantillas:** Jinja2 3.1.5
- **Frontend:** HTML5, CSS3, JavaScript Vanilla y Bootstrap 5 (vía CDN) + Bootstrap Icons
- **Gráficos:** Chart.js 4.4.x (vía CDN)
- **Generación de Reportes PDF:** ReportLab 4.3.1 (generación nativa en Python sin librerías externas del sistema)

---

## 📁 Estructura del Proyecto

```text
marroquineria/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada FastAPI, ciclo de vida y middlewares
│   ├── config.py            # Configuración basada en variables de entorno (.env)
│   ├── database.py          # Pool de conexiones ThreadedConnectionPool y context managers
│   ├── models/              # Modelos Pydantic (validación de payloads y respuestas)
│   │   ├── categoria.py
│   │   ├── material.py
│   │   ├── color.py
│   │   ├── tamano.py        # Tabla 'tamano' (sin ñ)
│   │   ├── proveedor.py
│   │   ├── medio_pago.py
│   │   ├── producto.py
│   │   ├── variante.py
│   │   ├── venta.py
│   │   ├── compra.py
│   │   └── devolucion.py
│   ├── repositories/        # Consultas SQL directas con parámetros (%s)
│   │   ├── categoria_repo.py
│   │   ├── material_repo.py
│   │   ├── color_repo.py
│   │   ├── tamano_repo.py
│   │   ├── proveedor_repo.py
│   │   ├── medio_pago_repo.py
│   │   ├── producto_repo.py
│   │   ├── variante_repo.py
│   │   ├── venta_repo.py
│   │   ├── compra_repo.py
│   │   ├── devolucion_repo.py
│   │   ├── dashboard_repo.py
│   │   └── reporte_repo.py
│   ├── services/            # Lógica de negocio y transacciones multi-tabla
│   │   ├── producto_service.py
│   │   ├── stock_service.py
│   │   ├── venta_service.py
│   │   ├── compra_service.py
│   │   ├── devolucion_service.py
│   │   └── reporte_service.py
│   ├── routers/             # Rutas y controladores de FastAPI
│   │   ├── dashboard.py
│   │   ├── abm.py
│   │   ├── productos.py
│   │   ├── stock.py
│   │   ├── ventas.py
│   │   ├── compras.py
│   │   ├── devoluciones.py
│   │   └── reportes.py
│   ├── templates/           # Plantillas Jinja2 (Bootstrap 5)
│   │   ├── base.html        # Layout maestro, sidebar y contenedor de toasts
│   │   ├── dashboard.html   # Gráfico Chart.js, KPIs y stock crítico
│   │   ├── abm/             # CRUD de entidades simples
│   │   ├── productos/       # Catálogo, alta/edición y detalle con variantes
│   │   ├── stock/           # Listado de variantes con edición en línea
│   │   ├── ventas/          # POS 3 paneles, comprobante imprimible e historial
│   │   ├── compras/         # Alta de compra, comprobante e historial
│   │   ├── devoluciones/    # Asistente de devolución/cambio e historial
│   │   └── reportes/        # Vista por pestañas y exportación
│   └── static/              # Archivos estáticos
│       ├── css/custom.css   # Estilos, tema oscuro y reglas @media print
│       └── js/
│           ├── theme.js     # Alternancia de tema claro/oscuro
│           ├── main.js      # Atajos globales (F2, ESC) y toasts
│           └── pos.js       # Carrito y cálculos dinámicos del POS
├── docs/                    # Fuente de verdad de la BD (DDL y DML)
│   ├── ddl_tif.sql
│   └── dml-poblado_tif.sql
├── logs/                    # Registro de actividad rotativo (app.log)
├── requirements.txt         # Dependencias fijadas a versiones estables
├── .env.example             # Plantilla de variables de entorno
├── run.py                   # Script de inicio del servidor
├── README.md                # Esta guía técnica
└── MANUAL_USUARIO.md        # Manual operativo para el personal del negocio
```

---

## ⚙️ Requisitos Previos

- **Python 3.11 o superior** instalado en el sistema.
- **PostgreSQL 14 o superior** instalado y en ejecución en el puerto `5432` (o configurado).

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar o posicionarse en el directorio del proyecto
```bash
cd "c:\Users\augus\OneDrive\Desktop\bases de datos\base-de-datos-marroquineria"
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias fijadas
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos PostgreSQL
Si la base de datos `marroquineria` ya fue creada y poblada, puedes saltear este paso. Si necesitas recrearla desde cero, ejecuta con tu cliente `psql`:

```bash
# Crear base de datos
createdb -U postgres marroquineria

# Ejecutar DDL (creación exacta de las 13 tablas)
psql -U postgres -d marroquineria -f docs/ddl_tif.sql

# Ejecutar DML (datos iniciales de prueba)
psql -U postgres -d marroquineria -f docs/dml-poblado_tif.sql
```

> [!IMPORTANT]
> La tabla de talles se denomina estrictamente `tamano` (sin ñ) y sus columnas son `id_tamano` y `nombre_tamano`. No se utiliza `tamaño` para garantizar compatibilidad nativa con PostgreSQL sin requerir comillas dobles.

### 5. Configurar el archivo `.env`
Copia el archivo de plantilla `.env.example` y crea tu `.env`:

En Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

Edita `.env` con los datos de tu PostgreSQL:
```ini
# Configuración de Base de Datos PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=marroquineria
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_MIN_CONN=1
DB_MAX_CONN=10

# Servidor Web
APP_HOST=127.0.0.1
APP_PORT=8000
DEBUG=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 6. Ejecutar la aplicación
Ejecuta el script de arranque:
```bash
python run.py
```

O directamente mediante Uvicorn:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Abre tu navegador en: **`http://localhost:8000`**

---

## 🖥️ Módulos y Pantallas del Sistema

### 1. Dashboard (`/dashboard` y `/`)
- **Tarjetas superiores (KPIs):** Total facturado hoy, total facturado en el mes, ticket promedio por venta y cantidad de artículos en stock crítico.
- **Gráfico de líneas interactivo (Chart.js):** Curva de facturación diaria de los últimos 30 días continuos con tooltips monetarios.
- **Tabla de stock crítico:** Alerta visual resaltada en rojo (`row-stock-critical`) con las variantes cuyo stock actual es menor o igual al mínimo.
- **Últimas 5 ventas:** Listado con enlace directo para visualizar o reimprimir el comprobante.

### 2. Gestión de Productos (`/productos`)
- Listado con filtros combinados por categoría, material y buscador de texto.
- Formulario de alta y edición con advertencia visual en vivo si `precio_lista < precio_costo`.
- **Vista de Detalle (`/productos/{id}`):** Ficha comercial con margen de ganancia calculado y tabla de variantes donde se pueden crear o modificar colores y talles del producto.

### 3. Gestión de Stock y Variantes (`/stock`)
- Listado general de todas las variantes del negocio con filtros por producto, color, talle y switch de **"Solo Stock Bajo"**.
- **Edición en línea (In-line):** Permite modificar directamente en la tabla el `stock_actual` y `stock_minimo` y guardar de forma asíncrona mediante fetch (`PUT /stock/{id}`) con notificación Toast sin recargar la página.
- **Resaltado inteligente:** Filas rojas para stock crítico (`<= stock_minimo`) y amarillas para reposición cercana (`<= stock_minimo * 1.5`).

### 4. Punto de Venta POS (`/ventas/pos`)
- **Panel Izquierdo:** Buscador de productos en tiempo real y selector de categoría.
- **Panel Central:** Carrito interactivo con ajuste de cantidades con validación de stock disponible.
- **Panel Derecho:** Selector de medio de pago con recálculo dinámico en pantalla:
  - Efectivo / Transferencia: **-20.00%** de descuento.
  - Débito / Crédito: **0.00%**.
  - Muestra el subtotal de lista, el ajuste monetario y el total final a cobrar.
- **Confirmación Transaccional:** Descuenta automáticamente el stock de cada variante vendida dentro de una transacción atómica.
- **Comprobante Interno (`/ventas/{id}/comprobante`):** Ticket no fiscal con botón de impresión directa (`window.print()`).

### 5. Registro de Compras (`/compras/nueva` e `/compras/historial`)
- Carga de mercadería ingresada por proveedor.
- Selector de variante con precarga automática del precio de costo de referencia.
- Al confirmar la compra, se ejecuta una transacción atómica que genera el detalle y **suma el stock** físico a cada variante.

### 6. Devoluciones, Cambios y Reparaciones (`/devoluciones/nueva` e `/devoluciones/historial`)
- Asistente guiado: búsqueda de venta original por ID y selección del artículo.
- Validación estricta: no permite devolver más unidades que las vendidas originalmente descontando devoluciones previas.
- **Lógica de negocio según motivo:**
  - `DEVOLUCION`: Suma el stock a la variante devuelta y reembolsa el dinero.
  - `CAMBIO`: Requiere seleccionar la nueva variante entregada. Verifica disponibilidad de stock en la variante nueva, suma stock a la devuelta, descuenta stock de la nueva y calcula automáticamente la diferencia económica:
    $$\text{diferencia} = (\text{precio\_variante\_nueva} - \text{precio\_cobrado\_original}) \times \text{cantidad}$$
  - `REPARACION`: Registra la orden de taller sin modificar el inventario.

### 7. Reportes y Estadísticas (`/reportes`)
Pestañas interactivas con filtros de fechas y exportación en **CSV** (compatible con Excel) y **PDF** (diseño vectorial ReportLab):
1. Ventas por período agrupadas por día.
2. Top 10 productos más vendidos.
3. Ventas por medio de pago.
4. Compras por proveedor.
5. Devoluciones agrupadas por motivo.
6. Stock valorizado al costo con capital total inmovilizado.
7. Variantes en stock crítico ordenadas por faltante.

### 8. ABMs Básicos (`/categorias`, `/materiales`, `/colores`, `/tamanos`, `/proveedores`, `/medios-pago`)
- CRUD completo para cada tabla simple con paginación, buscador y modales de edición.
- **Protección de Integridad:** Control de unicidad en nombres/CUIT y verificación previa de claves foráneas antes de eliminar (*"No se puede eliminar porque está siendo usado por X registros"*).

---

## ⌨️ Atajos de Teclado Globales

| Tecla | Acción |
| :--- | :--- |
| **`F2`** | Abre inmediatamente la pantalla de **Nueva Venta (POS)** desde cualquier lugar. |
| **`ESC`** | Cierra cualquier ventana modal o diálogo abierto. |
| **`Enter`** (en buscador POS) | Agrega automáticamente al carrito la primera variante disponible del primer producto encontrado. |

---

## ❓ Solución de Problemas Comunes

1. **Error de conexión a la base de datos (`could not connect to server`):**
   - Verifica que el servicio de PostgreSQL esté iniciado:
     En Windows: `Get-Service postgresql*` o desde el panel de Servicios (`services.msc`).
   - Verifica que el usuario, contraseña y base de datos en `.env` sean idénticos a los de tu instalación local.
2. **Error al eliminar un registro (`Registro en uso`):**
   - El sistema protege la base de datos de inconsistencias. Si una categoría, material, color, tamaño, proveedor o medio de pago está referenciado por productos o ventas existentes, no podrá ser eliminado hasta que se quiten dichas referencias.
3. **El puerto 8000 está ocupado:**
   - Puedes iniciar la aplicación en otro puerto cambiando `APP_PORT=8080` en el archivo `.env` o ejecutando:
     ```bash
     uvicorn app.main:app --port 8080 --reload
     ```
4. **Archivo de logs:**
   - La aplicación genera un registro de eventos rotativo en `logs/app.log`. Consúltalo ante cualquier anomalía para obtener el detalle de la excepción.
