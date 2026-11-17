import os

content = """# 🎙️ GUION HABLADO OFICIAL (DIVISIÓN 50 / 50)
### Sistema de Gestión Integral para Marroquinería — Proyecto Bases de Datos

> **Disertantes:** Augusto Barzola & Lucas Duarte  
> **Duración total:** 12 a 14 minutos (~6 a 7 minutos cada uno)  
> **Tono:** Académico, profesional, seguro y dinámico

---

## 📊 TABLA DE DISTRIBUCIÓN EQUITATIVA (50% / 50%)

| Bloque | Disertante | Diapositivas | Temas Evaluados por la Cátedra | Tiempo Estimado |
|---|---|---|---|---|
| **PRIMERA MITAD** | **Augusto Barzola** | **Slides 1 a 7** (7 diapositivas) | • Portada y presentación inicial<br>• Agenda de la exposición<br>• Problema del negocio y Solución Full Stack<br>• Arquitectura del Sistema (Capas: PostgreSQL + FastAPI + Jinja2)<br>• Modelo de Datos — DER (13 tablas)<br>• Normalización en Tercera Forma Normal (3FN)<br>• Triggers de Stock (PL/pgSQL en detalle_venta y detalle_compra) | **~6.5 minutos** |
| **SEGUNDA MITAD** | **Lucas Duarte** | **Slides 8 a 13** (6 diapositivas) | • Integridad en Devoluciones (FK compuesta)<br>• Consultas Complejas y Álgebra Relacional (Push-Down)<br>• SQL Directo (psycopg2) vs ORM (justificación)<br>• Demostración UI/UX (Modal Ticket POS y Dashboard expandible)<br>• Metodología de desarrollo asistido con IA<br>• Conclusiones, lecciones aprendidas y preguntas | **~6.5 minutos** |

---

# ═════════════════════════════════════════════
# PARTE I — PRIMERA MITAD: AUGUSTO BARZOLA (Slides 1 a 7)
# ═════════════════════════════════════════════

---

### 🔹 SLIDE 1: PORTADA
⏱️ **Tiempo sugerido:** ~30 segundos  
🎤 **Habla:** Augusto Barzola

> "Buenos días / buenas tardes profesor y compañeros. Somos **Augusto Barzola** y **Lucas Duarte**, y hoy les vamos a presentar nuestro proyecto final para la materia Bases de Datos.
>
> El sistema se titula **'Sistema de Gestión Integral para Marroquinería'**: una solución Full Stack construida desde el diseño formal relacional en PostgreSQL, backend en Python con FastAPI y psycopg2, y una interfaz web moderna en modo oscuro con estética glassmorphism.
>
> En los próximos minutos vamos a mostrar cómo la base de datos garantiza por sí misma la integridad del negocio y cómo optimizamos las consultas más exigentes."

---

### 🔹 SLIDE 2: ÍNDICE / AGENDA
⏱️ **Tiempo sugerido:** ~30 segundos  
🎤 **Habla:** Augusto Barzola

> "Esta es la estructura de nuestra presentación. La dividimos exactamente en dos bloques continuos para que sea dinámica y clara:
>
> • En la primera mitad, yo voy a cubrir el problema de negocio, la arquitectura del sistema, el modelo relacional de 13 tablas en 3FN y los triggers de actualización automática de stock en PostgreSQL.
>
> • En la segunda mitad, Lucas explicará la integridad estricta en devoluciones con clave foránea compuesta, la optimización matemática con Álgebra Relacional, la justificación de SQL directo frente a un ORM, la interfaz de usuario y las conclusiones finales."

---

### 🔹 SLIDE 3: DESCRIPCIÓN DEL PROBLEMA Y SOLUCIÓN
⏱️ **Tiempo sugerido:** ~1 minuto  
🎤 **Habla:** Augusto Barzola

> "Para contextualizar el negocio: una marroquinería comercializa artículos de cuero como carteras, mochilas, cinturones y billeteras. Su principal desafío operativo radica en que cada producto se diversifica en múltiples variantes según color, material y tamaño.
>
> En la mayoría de las PYMEs, esta gestión se hace en cuadernos o planillas de cálculo desarticuladas, lo que ocasiona:
> 1. Descuadres constantes de inventario y roturas de stock no detectadas a tiempo.
> 2. Devoluciones sin comprobación estricta que provocan inconsistencias contables.
> 3. Falta total de información en tiempo real sobre ventas diarias y productos críticos.
>
> Nuestra respuesta fue desarrollar un **Sistema de Gestión Integral centralizado en PostgreSQL**, donde la base de datos opera como la única fuente de verdad: el motor protege su propia información con triggers y restricciones, brindándole al comerciante un Punto de Venta ágil y un Dashboard analítico en vivo."

---

### 🔹 SLIDE 4: ARQUITECTURA DEL SISTEMA — STACK TECNOLÓGICO
⏱️ **Tiempo sugerido:** ~1 minuto  
🎤 **Habla:** Augusto Barzola

> "La arquitectura del sistema sigue un modelo por capas limpio, robusto y desacoplado:
>
> 1. En la base del stack tenemos **PostgreSQL**: nuestro motor relacional ACID, donde residen las 13 tablas, las foreign keys, los constraints CHECK y los triggers en PL/pgSQL.
> 2. En la capa de backend implementamos **FastAPI con Python 3.11**. Lo seleccionamos por su velocidad asíncrona, bajo consumo de recursos y validación estricta de esquemas.
> 3. Para la conexión a la base de datos optamos por **psycopg2 directo con un ThreadedConnectionPool**, permitiendo transacciones explícitas sin la sobrecarga de un ORM.
> 4. Y en la presentación usamos **Jinja2** para renderizado en servidor junto a **Bootstrap 5**, logrando una interfaz en modo oscuro con efecto glassmorphism, moderna y muy fluida.
>
> Es una estructura simple y confiable, sin capas intermedias innecesarias."

---

### 🔹 SLIDE 5: MODELO DE DATOS — DIAGRAMA ENTIDAD-RELACIÓN (13 TABLAS)
⏱️ **Tiempo sugerido:** ~1.5 minutos  
🎤 **Habla:** Augusto Barzola

> "El modelo relacional está compuesto por 13 tablas organizadas en tres categorías bien definidas:
>
> • **Entidades maestras:** `producto`, `variante_producto`, `venta` y `compra`. Constituyen el núcleo transaccional del negocio.
> • **Tablas de detalle:** `detalle_venta`, `detalle_compra` y `devolucion`. Representan los ítems individuales de cada operación.
> • **Tablas de dominio o catálogo:** `categoria`, `material`, `color`, `tamano`, `proveedor` y `medio_pago`.
>
> Un punto de rigor técnico clave es que las tablas de detalle utilizan **Claves Primarias Compuestas**, como `(id_venta, renglon_venta)`. Esto garantiza matemáticamente que dentro de un mismo comprobante cada renglón es único e irrepetible. Además, todas las relaciones cuentan con Foreign Keys que previenen registros huérfanos."

---

### 🔹 SLIDE 6: NORMALIZACIÓN EN TERCERA FORMA NORMAL (3FN)
⏱️ **Tiempo sugerido:** ~1.5 minutos  
🎤 **Habla:** Augusto Barzola

> "Un requisito central de la cátedra es la normalización. Nuestro esquema cumple rigurosamente con la **Tercera Forma Normal (3FN)**:
>
> • **Primera Forma Normal (1FN):** Todos los atributos son atómicos y no existen grupos repetitivos ni arrays dentro de las columnas.
> • **Segunda Forma Normal (2FN):** En tablas con clave compuesta, los atributos dependen de la clave primaria completa y no de una parte de ella.
> • **Tercera Forma Normal (3FN):** No existen dependencias transitivas. Ningún atributo no-clave depende funcionalmente de otro atributo no-clave.
>
> Ejemplo práctico: en lugar de guardar el color o el material como texto en la tabla `variante_producto` —lo que provocaría anomalías de actualización y duplicación masiva— creamos tablas independientes para `color` y `material`, referenciadas únicamente por su ID. Si se modifica un nombre, se realiza un solo `UPDATE` en una sola fila, garantizando consistencia absoluta en el historial."

---

### 🔹 SLIDE 7: TRIGGERS DE STOCK: LA BASE DE DATOS SE PROTEGE A SÍ MISMA
⏱️ **Tiempo sugerido:** ~1.5 minutos  
🎤 **Habla:** Augusto Barzola

> "Para cerrar mi bloque, quiero explicar uno de los puntos más relevantes del sistema: los **Triggers en PostgreSQL**.
>
> En nuestra arquitectura, el control de inventario **NO se delega a la aplicación ni al frontend**. La base de datos se protege a sí misma de forma autónoma:
>
> • Al realizarse un `INSERT` en `detalle_venta`, el trigger `trg_stock_venta` dispara una función en PL/pgSQL que decrementa automáticamente el `stock_actual` de esa variante.
> • De forma inversa, al registrarse un `INSERT` en `detalle_compra`, otro trigger incrementa el stock al recibir mercadería del proveedor.
>
> ¿Por qué es crucial? Porque si alguien inserta registros directamente desde pgAdmin, o mediante un script de importación, el trigger se ejecuta exactamente igual. La integridad del inventario no depende del canal de entrada. En el código PL/pgSQL utilizamos la variable especial `NEW.cantidad` para capturar el valor exacto del renglón recién insertado."

---

### 🔄 [FRASE DE TRANSICIÓN — AUGUSTO CEDE LA PALABRA]:
> **Augusto:** *"Habiendo visto el modelo de datos, la normalización y los triggers, le paso la palabra a Lucas, quien continuará con la integridad en devoluciones, el álgebra relacional, la interfaz y las conclusiones."*

---

# ═════════════════════════════════════════════
# PARTE II — SEGUNDA MITAD: LUCAS DUARTE (Slides 8 a 13)
# ═════════════════════════════════════════════

---

### 🔹 SLIDE 8: TABLA DEVOLUCIÓN: INTEGRIDAD CON CLAVE FORÁNEA COMPUESTA
⏱️ **Tiempo sugerido:** ~1.5 minutos  
🎤 **Habla:** Lucas Duarte

> "Gracias Augusto. Continuando con la solidez de la base de datos, quiero destacar el diseño de la tabla `devolucion`, que resuelve un problema crítico de integridad que una foreign key simple no puede solucionar.
>
> El problema es: **¿cómo evitamos que se devuelva un ítem o producto que jamás formó parte de esa venta?**
>
> Si hubiéramos usado una clave foránea simple apuntando a `id_venta`, la base de datos solo verificaría que la venta existió, pero permitiría registrar la devolución de cualquier producto ficticio o de otra venta.
>
> Nuestra solución fue definir una **Clave Foránea Compuesta** que referencia directamente al par `(id_venta, renglon_venta)` de `detalle_venta`. De este modo, el motor valida obligatoriamente que ese renglón exacto haya sido vendido en ese ticket. Si no existe, PostgreSQL rechaza físicamente el `INSERT` con un error de integridad referencial. Es una garantía a nivel motor, sin depender de validaciones manuales de software."

---

### 🔹 SLIDE 9: CONSULTAS COMPLEJAS Y ÁLGEBRA RELACIONAL (PUSH-DOWN)
⏱️ **Tiempo sugerido:** ~2 minutos  
🎤 **Habla:** Lucas Duarte

> "Otro aspecto fundamental que evaluó la cátedra fueron las **Consultas Complejas y el Álgebra Relacional**. Desarrollamos 6 consultas analíticas con múltiples JOINs y agregaciones.
>
> Para optimizar la consulta más costosa —que calcula la recaudación del día agrupada por producto uniendo `venta`, `detalle_venta`, `variante` y `producto`— modelamos su **Árbol de Álgebra Relacional**.
>
> Un árbol ingenuo une primero todas las ventas históricas con todos los detalles y variantes, generando una tabla intermedia inmensa, para recién al final aplicar el filtro de fecha. Esto consume memoria innecesaria y ralentiza el motor.
>
> Nosotros aplicamos formalmente la técnica de **Push-Down de Selecciones**: empujar el operador de filtro sigma `(fecha = hoy)` hacia las hojas del árbol, antes de realizar los JOINs. Al filtrar las ventas del día primero, el operador JOIN procesa únicamente los 20 comprobantes de hoy en vez de miles de registros históricos. Esta reducción drástica del conjunto intermedio es el principio de optimización que usan los motores de bases de datos profesionales."

---

### 🔹 SLIDE 10: SQL DIRECTO CON PSYCOPG2 VS ORM
⏱️ **Tiempo sugerido:** ~1 minuto  
🎤 **Habla:** Lucas Duarte

> "Una decisión arquitectónica importante que tomamos fue prescindir de un ORM y utilizar **psycopg2 de forma directa**.
>
> Aunque herramientas como SQLAlchemy facilitan el prototipado rápido, introducen capas de abstracción opacas, generan consultas N+1 difíciles de predecir y complican el control fino de transacciones.
>
> Al trabajar con SQL puro y psycopg2:
> 1. Escribimos y optimizamos cada consulta a mano con pleno control del plan de ejecución.
> 2. Administramos transacciones explícitas con bloques `BEGIN`, `COMMIT` y `ROLLBACK` ante cualquier excepción.
> 3. Implementamos un `ThreadedConnectionPool` que gestiona de 2 a 10 conexiones seguras para usuarios concurrentes.
> 4. Y académicamente, demostramos dominio del lenguaje SQL estándar y de las capacidades nativas de PostgreSQL."

---

### 🔹 SLIDE 11: INTERFAZ DE USUARIO: POS Y DASHBOARD
⏱️ **Tiempo sugerido:** ~1.5 minutos  
🎤 **Habla:** Lucas Duarte

> "Pasando a la experiencia del usuario, diseñamos dos módulos centrales orientados a la velocidad operativa y a prevenir errores humanos:
>
> • **Punto de Venta (POS):** Permite buscar productos en tiempo real, filtrar por variantes y seleccionar el medio de pago con recargos o descuentos automáticos. Pero lo más importante es que agregamos un **Modal de Confirmación con formato de Ticket Fiscal**: antes de guardar la venta, el vendedor visualiza el detalle completo de ítems, cantidades y total. Si detecta un error puede cancelar en el momento, evitando transacciones erróneas y posteriores devoluciones.
>
> • **Dashboard Dinámico:** Cuenta con métricas clave en vivo (ventas de hoy, stock crítico). Cada métrica es una **Tarjeta Expandible**: al hacer clic, por ejemplo en 'Stock Bajo', la tarjeta se despliega suavemente y muestra la tabla con todos los productos bajo el stock mínimo.
>
> Toda la interfaz utiliza modo oscuro con estética glassmorphism, brindando una experiencia moderna y cómoda para largas jornadas de trabajo."

---

### 🔹 SLIDE 12: DESARROLLO ASISTIDO POR IA — PROTOCOLO POR FASES
⏱️ **Tiempo sugerido:** ~1 minuto  
🎤 **Habla:** Lucas Duarte

> "En cuanto a la metodología, aplicamos un desarrollo asistido por Inteligencia Artificial utilizando **Antigravity de Google DeepMind**, siguiendo un protocolo estructurado en 5 fases:
>
> 1. **Fase 1:** Modelado conceptual y DER en 3FN.
> 2. **Fase 2:** Esquema DDL, constraints y triggers en PL/pgSQL.
> 3. **Fase 3:** Backend en FastAPI con pool de conexiones y endpoints REST.
> 4. **Fase 4:** Frontend en Jinja2 con modales y componentes expandibles.
> 5. **Fase 5:** Pruebas de concurrencia, sincronización de secuencias y auditoría de integridad.
>
> Queremos destacar que la IA actuó como un co-piloto técnico que aceleró la escritura de código, pero las decisiones de diseño, la lógica relacional y la validación de cada línea fueron dirigidas y controladas 100% por nosotros."

---

### 🔹 SLIDE 13: CONCLUSIONES Y CIERRE
⏱️ **Tiempo sugerido:** ~1 minuto  
🎤 **Habla:** Lucas Duarte

> "Para cerrar nuestra exposición, queremos compartir los aprendizajes y logros principales:
>
> 1. Construimos un sistema Full Stack completamente funcional y adaptado a las necesidades reales de una marroquinería.
> 2. La base de datos no es un simple repositorio: es un sistema inteligente y autosuficiente gracias a sus triggers y claves foráneas compuestas.
> 3. Confirmamos que la normalización y el álgebra relacional no son meros ejercicios teóricos, sino las bases fundamentales para evitar bugs graves y lograr que una aplicación escale.
> 4. Demostramos que el control directo sobre el motor SQL supera la comodidad de las abstracciones ciegas.
>
> Les agradecemos mucho por su tiempo y quedamos a disposición de la cátedra para responder todas sus preguntas."
"""

with open("2_Guion_Hablado.md", "w", encoding="utf-8") as f:
    f.write(content)

print("2_Guion_Hablado.md successfully updated with 50/50 split!")
