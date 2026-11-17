# PRESENTACION FINAL - SISTEMA DE GESTION PARA MARROQUINERIA
### Estructura de Diapositivas + Guion Hablado Completo

> **Formato:** PowerPoint / Google Slides
> **Duracion estimada:** 13-15 minutos
> **Integrantes:** 2 (Division equitativa)
> **Tono:** Profesional, academico, seguro y dinamico

---

# ===============================
# PARTE 1 - ESTRUCTURA DE DIAPOSITIVAS
# ===============================

---

## SLIDE 1 - PORTADA

**Titulo principal:**
> Sistema de Gestion Integral para Marroquineria
> *Diseno, Implementacion y Optimizacion de una Base de Datos Relacional*

**Subtitulo:** Proyecto Final - Bases de Datos

**Contenido:**
- Integrante 1: [Nombre]
- Integrante 2: [Nombre]
- Universidad / Materia / Anio

**Imagen sugerida:**
- Logo del sistema (logo.jpg) centrado
- Captura del Dashboard o POS como fondo con opacidad baja
- Efecto glassmorphism que refleje el estilo visual del sistema

---

## SLIDE 2 - INDICE / AGENDA

**Titulo:** iQue vamos a ver hoy?

**Vinetas:**
1. Descripcion del problema y la solucion
2. Arquitectura del sistema (stack tecnologico)
3. Modelo de datos - Diagrama Entidad-Relacion
4. Normalizacion en Tercera Forma Normal (3FN)
5. Triggers de base de datos
6. Diseno de la tabla Devolucion
7. Consultas complejas y Algebra Relacional
8. SQL directo vs ORM - Decision tecnica
9. Interfaz: POS y Dashboard
10. Desarrollo asistido por IA
11. Conclusiones

**Imagen sugerida:**
- Linea de tiempo horizontal o lista numerada con iconos simples

---

## SLIDE 3 - DESCRIPCION DEL PROBLEMA Y SOLUCION

**Titulo:** El Problema y Nuestra Solucion

**Vinetas - Problema:**
- Gestion manual de stock -> errores humanos, mercaderia perdida
- Sin trazabilidad de ventas y compras
- Devoluciones no controladas -> inconsistencias contables
- Sin visibilidad del negocio en tiempo real

**Vinetas - Solucion:**
- Sistema Full Stack con base de datos PostgreSQL centralizada
- Modulos: POS, Dashboard, Reportes, Stock, Proveedores
- Integridad de datos garantizada por la propia base (triggers, FKs compuestas)
- Interfaz web moderna accesible desde cualquier dispositivo

**Imagen sugerida:**
- Dos columnas: izquierda "Antes" (planilla Excel), derecha "Despues" (captura del Dashboard)

---

## SLIDE 4 - ARQUITECTURA DEL SISTEMA

**Titulo:** Stack Tecnologico - Arquitectura en Capas

**Vinetas:**
- Base de Datos: PostgreSQL - 13 tablas, relaciones, constraints, triggers
- Backend: Python + FastAPI - API REST, logica de negocio
- Conector BD: psycopg2 - Conexion directa sin ORM (ThreadedConnectionPool)
- Frontend: Jinja2 (templates server-side) + Bootstrap 5
- Estilo UI: Modo oscuro + Glassmorphism

**Diagrama sugerido:**

```
[ Navegador Web (Bootstrap 5 + Jinja2) ]
              v HTTP / HTML
       [ FastAPI (Python) ]
              v psycopg2
       [ PostgreSQL (13 tablas) ]
```

---

## SLIDE 5 - MODELO DE DATOS - DIAGRAMA ENTIDAD-RELACION

**Titulo:** Modelo de Datos - 13 Tablas Normalizadas

**Vinetas:**
- Entidades principales: producto, variante_producto, venta, compra
- Entidades de detalle: detalle_venta, detalle_compra, devolucion
- Tablas de dominio: categoria, material, color, tamano, proveedor, medio_pago
- Claves primarias compuestas en tablas de detalle y devolucion
- Restricciones NOT NULL, CHECK, UNIQUE aplicadas

**Imagen sugerida:**
- Captura del DER completo (generado desde pgAdmin o dbdiagram.io)
- Resaltar con color las tablas criticas: detalle_venta, devolucion, variante_producto

---

## SLIDE 6 - NORMALIZACION (3FN)

**Titulo:** Normalizacion en Tercera Forma Normal

**Vinetas:**
- 1FN: Todos los atributos son atomicos, no hay grupos repetitivos
- 2FN: Cada atributo no-clave depende de la clave primaria completa
- 3FN: No existen dependencias transitivas
- Ejemplo: color, material, tamano -> tablas propias (no texto repetido en variante_producto)
- Beneficio: sin redundancia, actualizaciones consistentes, sin anomalias

**Tabla de ejemplo:**

| Sin normalizar | Con 3FN |
|---|---|
| variante(id, color="Negro", material="Cuero") | variante(id, id_color, id_material) |
| Color repetido en cada fila | Color definido UNA vez en tabla color |

---

## SLIDE 7 - TRIGGERS DE BASE DE DATOS

**Titulo:** Triggers - La Base de Datos se Protege a Si Misma

**Vinetas:**
- Los triggers actualizan el stock AUTOMATICAMENTE al registrar movimientos
- detalle_venta INSERT -> decrementa stock_actual en variante_producto
- detalle_compra INSERT -> incrementa stock_actual en variante_producto
- La integridad NO depende de la aplicacion - opera a nivel de motor de BD
- Proteccion contra errores de programacion, accesos directos o scripts

**Codigo SQL:**

```sql
CREATE OR REPLACE FUNCTION actualizar_stock_venta()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id_variante = NEW.id_variante;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_stock_venta
AFTER INSERT ON detalle_venta
FOR EACH ROW EXECUTE FUNCTION actualizar_stock_venta();
```

**Imagen sugerida:**
- Diagrama de flujo: INSERT en detalle_venta -> TRIGGER se dispara -> UPDATE en variante_producto

---

## SLIDE 8 - DISENO DE LA TABLA DEVOLUCION

**Titulo:** Tabla Devolucion - Integridad Referencial con FK Compuesta

**Vinetas:**
- Problema: iComo evitar devolver un producto que NO estaba en esa venta?
- Solucion: Clave foranea COMPUESTA que referencia detalle_venta(id_venta, renglon_venta)
- Si el par (id_venta, renglon_venta) no existe en detalle_venta -> la BD RECHAZA el INSERT
- Garantia imposible de lograr con una FK simple

**Codigo SQL:**

```sql
CREATE TABLE devolucion (
    id_devolucion    SERIAL PRIMARY KEY,
    id_venta         INTEGER NOT NULL,
    renglon_venta    INTEGER NOT NULL,
    cantidad_devuelta INTEGER NOT NULL CHECK (cantidad_devuelta > 0),
    motivo           TEXT,
    fecha_devolucion DATE DEFAULT CURRENT_DATE,

    CONSTRAINT fk_devolucion_detalle
        FOREIGN KEY (id_venta, renglon_venta)
        REFERENCES detalle_venta(id_venta, renglon_venta)
);
```

---

## SLIDE 9 - CONSULTAS COMPLEJAS Y ALGEBRA RELACIONAL

**Titulo:** Consultas Complejas - Algebra Relacional y Optimizacion

**Vinetas:**
- Se implementaron 6 consultas complejas con JOINs, agregaciones y subconsultas
- Se modelo el arbol de algebra relacional para analizar el plan de ejecucion
- Tecnica aplicada: Push-down de selecciones (filtrar primero, luego unir)
- Resultado: reduccion del tamano de tablas intermedias -> menos costo de computo

**Arbol de Algebra Relacional:**

```
          pi (Proyeccion: nombre, total_vendido)
                        |
          gamma (Agrupacion: SUM por producto)
                        |
                    JOIN
                   /     \
        sigma(fecha=hoy)   variante_producto
               |
          detalle_venta
               |
            venta
```

**Comparacion Push-Down:**

| Sin Push-Down | Con Push-Down |
|---|---|
| JOIN todas las tablas primero | Filtrar fecha = hoy ANTES del JOIN |
| Resultado intermedio: todas las ventas | Resultado intermedio: solo ventas de hoy |
| Costoso en volumen | Eficiente y escalable |

---

## SLIDE 10 - SQL DIRECTO vs ORM

**Titulo:** iPor que psycopg2 y no un ORM?

**Vinetas:**
- ORM (SQLAlchemy, Django ORM): abstraccion de alto nivel, SQL generado automaticamente
- psycopg2: acceso directo al motor PostgreSQL - control total
- Ventajas elegidas:
  - Control explicito de transacciones (BEGIN / COMMIT / ROLLBACK)
  - Pool de conexiones con ThreadedConnectionPool
  - Uso de cursores especializados (RealDictCursor)
  - Consultas optimizadas escritas a mano (sin SQL fantasma del ORM)
  - Transparencia total del codigo ejecutado

**Comparacion de codigo:**

```python
# ORM (SQLAlchemy) - opaco, genera SQL automaticamente
ventas = session.query(Venta).filter(Venta.fecha == hoy).all()

# psycopg2 - control total, explicito y optimizable
cur.execute("""
    SELECT v.id_venta, mp.nombre AS medio_pago, v.total
    FROM venta v
    JOIN medio_pago mp ON v.id_medio_pago = mp.id_medio_pago
    WHERE v.fecha = %s
""", (hoy,))
ventas = cur.fetchall()
```

---

## SLIDE 11 - INTERFAZ: POS Y DASHBOARD

**Titulo:** Interfaz de Usuario - Funcionalidad y Experiencia Visual

**Vinetas - POS:**
- Busqueda de productos en tiempo real
- Carrito dinamico con cantidades editables
- Modal de confirmacion con ticket resumido antes de cerrar venta
- Soporte para multiples medios de pago con descuento/recargo automatico

**Vinetas - Dashboard:**
- Tarjetas de metricas clave (ventas hoy, stock bajo, etc.)
- Tarjetas expandibles al clic con informacion detallada
- Transiciones CSS suaves (glassmorphism + modo oscuro)

**Imagenes sugeridas:**
- Captura del modal de confirmacion de venta (POS)
- Captura del Dashboard con una tarjeta expandida

---

## SLIDE 12 - DESARROLLO ASISTIDO POR IA

**Titulo:** Desarrollo Asistido por IA - Protocolo por Fases

**Vinetas:**
- Herramienta utilizada: Antigravity (Google DeepMind AI Assistant)
- Metodologia: protocolo de desarrollo estructurado por fases
  - Fase 1: Diseno del modelo de datos y DER
  - Fase 2: Generacion del esquema SQL y triggers
  - Fase 3: Backend FastAPI - rutas, controladores, logica de negocio
  - Fase 4: Frontend - templates Jinja2, componentes Bootstrap 5
  - Fase 5: Integracion, pruebas y correccion de errores
- Rol del equipo: toma de decisiones tecnicas, revision critica, validacion
- La IA como co-piloto, el equipo como arquitecto y decisor

**Imagen sugerida:**
- Diagrama de flujo de las 5 fases de desarrollo

---

## SLIDE 13 - CONCLUSIONES Y CIERRE

**Titulo:** Conclusiones - Lo que Logramos y lo que Aprendimos

**Vinetas - Logros:**
- Sistema funcional de gestion integral para una PYME real
- Base de datos normalizada en 3FN con 13 tablas
- Integridad garantizada a nivel de motor (triggers, FK compuestas)
- Consultas optimizadas con algebra relacional aplicada
- Interfaz moderna, usable y responsive

**Vinetas - Aprendizajes:**
- La normalizacion NO es solo teoria - evita bugs reales en produccion
- Los triggers son la ultima linea de defensa de la integridad de datos
- Elegir las herramientas correctas importa: psycopg2 > ORM para este caso
- El desarrollo asistido por IA acelera, pero no reemplaza el criterio tecnico

**Imagen sugerida:**
- Captura final del sistema completo (Dashboard visible)

---

# ===============================
# PARTE 2 - GUION HABLADO COMPLETO
# ===============================

> Convenciones:
> - INT. 1 -> Integrante 1 habla
> - INT. 2 -> Integrante 2 habla
> - [TRANSICION] -> Frase puente entre oradores
> - Tiempo estimado por slide indicado entre parentesis

---

## SLIDE 1 - PORTADA (~30 seg)

[INT. 1:]
"Buenos dias / buenas tardes. Somos [Nombre 1] y [Nombre 2], y hoy les vamos a presentar nuestro proyecto final para la materia Bases de Datos.

El proyecto se llama 'Sistema de Gestion Integral para Marroquineria' - un sistema Full Stack desarrollado desde cero, con base de datos relacional en PostgreSQL, backend en Python con FastAPI, y una interfaz web moderna.

En los proximos minutos vamos a recorrer las decisiones de diseno, los desafios tecnicos que encontramos, y como los resolvimos."

---

## SLIDE 2 - INDICE (~30 seg)

[INT. 1:]
"Esta es la agenda de hoy. Vamos a ir desde la descripcion del problema hasta las conclusiones, pasando por los puntos mas tecnicos del proyecto: el modelo de datos, los triggers, las consultas complejas y las decisiones de arquitectura.

Vamos a dividir la presentacion: yo voy a cubrir la base de datos, la normalizacion, los triggers y las consultas; y [Nombre 2] va a presentar la arquitectura del sistema, la interfaz de usuario y las conclusiones."

---

## SLIDE 3 - PROBLEMA Y SOLUCION (~1 min)

[INT. 1:]
"Empecemos por el contexto. Una marroquineria es un negocio que vende productos de cuero: carteras, billeteras, cinturones. Cada producto puede tener multiples variantes: distintos colores, materiales, tamanos.

El problema que identificamos es muy comun en las PYMEs: la gestion se hacia de forma manual, con planillas de Excel o incluso en papel. Esto genera errores de stock, ventas mal registradas, devoluciones sin control y nula visibilidad del negocio en tiempo real.

Nuestra solucion fue construir un sistema de gestion integral. Un sistema donde la base de datos garantiza la integridad de los datos por si misma, donde el vendedor puede operar desde una interfaz simple, y donde el duenio puede ver el estado del negocio en un Dashboard en tiempo real."

---

## SLIDE 4 - ARQUITECTURA (~1.5 min)

[TRANSICION - INT. 1 cede la palabra:]
"Para entender como esta construido el sistema, le paso la palabra a [Nombre 2], que va a explicar la arquitectura tecnica."

---

[INT. 2:]
"Gracias [Nombre 1].

El sistema sigue una arquitectura en capas clasica. En la base tenemos PostgreSQL, el motor de base de datos relacional que almacena todas las tablas, restricciones y logica de triggers.

Por encima, el backend esta desarrollado en Python usando FastAPI, un framework moderno y de alto rendimiento para construir APIs REST. La comunicacion entre el backend y la base de datos se hace con psycopg2, una libreria de conexion directa, sin ORM. Vamos a hablar de esa decision en detalle mas adelante.

En la capa de presentacion tenemos Jinja2, que genera las paginas HTML del lado del servidor, y Bootstrap 5 para el estilo visual. La interfaz usa modo oscuro con un efecto visual llamado glassmorphism - ese efecto de vidrio esmerilado que le da profundidad a los componentes.

Es una arquitectura simple, directa y eficiente - sin capas innecesarias que agreguen complejidad sin beneficio."

---

## SLIDE 5 - MODELO DE DATOS - DER (~1.5 min)

[TRANSICION - INT. 2 devuelve la palabra:]
"Con esa arquitectura clara, le devuelvo la palabra a [Nombre 1] para que nos explique el modelo de datos."

---

[INT. 1:]
"El modelo de datos tiene 13 tablas normalizadas. Voy a agruparlas en tres categorias para que sea mas facil de entender.

Las entidades principales son: producto, variante_producto, venta y compra. Estas son el nucleo del negocio.

Las tablas de detalle son: detalle_venta, detalle_compra y devolucion. Estas representan el contenido de cada transaccion: los items individuales de cada venta, compra o devolucion.

Y las tablas de dominio son aquellas que almacenan valores de referencia: categoria, material, color, tamano, proveedor y medio_pago.

Las tablas de detalle usan claves primarias compuestas. Por ejemplo, detalle_venta tiene como clave el par (id_venta, renglon_venta). Esto garantiza que dentro de una misma venta, cada item tiene un numero de renglon unico e irrepetible.

Pueden ver en el diagrama las relaciones entre las tablas. Lo importante es notar que practicamente todas las relaciones tienen restricciones de integridad referencial - foreign keys - que impiden dejar registros huerfanos."

---

## SLIDE 6 - NORMALIZACION (3FN) (~1.5 min)

[INT. 1:]
"Esto me lleva al tema de la normalizacion. El modelo esta en Tercera Forma Normal, o 3FN.

Para que este en 3FN, tenemos que satisfacer tres condiciones. Primero: todos los atributos son atomicos - no hay listas ni grupos repetitivos dentro de un campo. Segundo: cada atributo no-clave depende de la clave primaria completa, no de una parte de ella. Y tercero, que es el mas importante: no hay dependencias transitivas. Eso significa que un atributo no puede depender de otro atributo que no sea clave.

Ejemplo concreto: si tuvieramos el color del producto guardado como texto en la tabla variante_producto, escribiriamos 'Negro' en cada fila que tiene ese color. Si algun dia quisieramos renombrar ese color, tendriamos que actualizar cientos de filas, con el riesgo de inconsistencias.

En cambio, en nuestra base, color es una tabla separada con su propio id_color. La variante solo guarda la referencia. El color se define una sola vez, y se reutiliza por referencia. Eso es 3FN aplicada en la practica."

---

## SLIDE 7 - TRIGGERS (~2 min)

[INT. 1:]
"Ahora llegamos a uno de los puntos mas importantes del proyecto desde el punto de vista de la base de datos: los triggers.

Un trigger es un procedimiento almacenado que se ejecuta automaticamente cuando ocurre un evento en una tabla, como un INSERT, UPDATE o DELETE.

En nuestro sistema, implementamos triggers para mantener el stock actualizado automaticamente. La logica es la siguiente:

Cuando se inserta un registro en detalle_venta, es decir, cuando se vende un item, el trigger llama a una funcion que decrementa el stock_actual de esa variante de producto en la cantidad vendida.

Cuando se inserta un registro en detalle_compra, cuando llega mercaderia del proveedor, el trigger hace lo contrario: incrementa el stock.

Lo critico aqui es que esta logica vive en la base de datos, no en la aplicacion. iY por que importa esto? Porque si alguien accede directamente a la base de datos con una herramienta como pgAdmin, o si un script de migracion de datos inserta registros directo en la tabla, el trigger se dispara igual. La integridad del stock esta garantizada independientemente de como se acceda a los datos.

En el codigo que ven en pantalla, NEW.cantidad hace referencia al valor de la columna cantidad del registro recien insertado. Es la sintaxis estandar de PL/pgSQL para acceder a los valores nuevos dentro de un trigger."

---

## SLIDE 8 - TABLA DEVOLUCION (~1.5 min)

[INT. 1:]
"El otro diseno que quiero destacar es el de la tabla devolucion, porque resuelve un problema de integridad referencial que con una clave foranea simple NO se puede resolver.

El problema es este: si alguien quiere procesar una devolucion, necesitamos asegurarnos de que el item que se quiere devolver realmente pertenezca a esa venta. No puede volver un producto que nunca se vendio en esa transaccion.

Si usaramos solo una FK a id_venta, estariamos verificando que la venta existe, pero NO que ese item en particular estuvo en esa venta.

La solucion es una clave foranea compuesta que referencia el par (id_venta, renglon_venta) de la tabla detalle_venta. La base de datos, antes de permitir el INSERT en devolucion, verifica que ese par exacto exista en detalle_venta. Si no existe, rechaza la operacion con un error de integridad referencial.

Es una garantia que no depende de validaciones en el codigo de la aplicacion. La base de datos la enforce de manera nativa y automatica."

---

## SLIDE 9 - CONSULTAS Y ALGEBRA RELACIONAL (~2 min)

[INT. 1:]
"El ultimo punto tecnico de la base de datos son las consultas complejas. Implementamos seis consultas con multiples JOINs, agregaciones con GROUP BY y subconsultas.

Para analizar y optimizar una de las mas costosas, que une venta, detalle_venta y variante_producto para calcular el total vendido por producto hoy, construimos un arbol de algebra relacional.

En algebra relacional, los operadores son: sigma para seleccion, pi para proyeccion, gamma para agrupacion, y el simbolo de join para las uniones.

El arbol sin optimizar haria primero todos los JOINs, uniendo todas las ventas con todos los detalles con todas las variantes, y despues aplicaria el filtro de fecha. Eso genera una tabla intermedia gigante que luego se descarta en su mayor parte.

La optimizacion que aplicamos se llama push-down de selecciones: bajar los filtros al nivel mas bajo posible del arbol, antes de cualquier JOIN. Asi, si filtramos por fecha = hoy antes de hacer el JOIN, la tabla que ingresa al JOIN ya tiene solo las ventas del dia, que pueden ser 20 filas en vez de miles.

La reduccion del tamano de los resultados intermedios es directamente proporcional a la mejora de rendimiento. Esta tecnica es la base del optimizador de consultas de cualquier motor de base de datos moderno."

---

## SLIDE 10 - SQL DIRECTO vs ORM (~1 min)

[INT. 1:]
"Para cerrar mi parte, quiero explicar una decision de arquitectura que tomamos y que vale la pena justificar: no usamos ORM.

Un ORM como SQLAlchemy o Django ORM genera SQL automaticamente a partir de clases de Python. Es conveniente para el desarrollo rapido, pero tiene costos: genera SQL que no siempre es optimo, agrega una capa de abstraccion que oculta lo que pasa en la base de datos, y limita el control sobre las transacciones.

Nosotros usamos psycopg2 directamente. Esto nos da control total. Podemos escribir exactamente el SQL que queremos, podemos usar RealDictCursor para obtener resultados como diccionarios, manejamos explicitamente el BEGIN, COMMIT y ROLLBACK de cada transaccion, y usamos ThreadedConnectionPool para gestionar eficientemente multiples conexiones concurrentes.

Para un proyecto academico donde el objetivo es demostrar dominio de SQL y bases de datos, esta eleccion tambien tiene un valor pedagogico: todo lo que hacemos es visible y explicito."

---

## SLIDE 11 - INTERFAZ: POS Y DASHBOARD (~1.5 min)

[TRANSICION - INT. 1 cede la palabra:]
"Con eso termino mi parte sobre la base de datos. Le paso la palabra nuevamente a [Nombre 2] para que nos muestre la interfaz del sistema."

---

[INT. 2:]
"Gracias [Nombre 1]. Vamos a ver el sistema en accion desde el lado del usuario.

El Punto de Venta, o POS, es el modulo mas usado en el dia a dia. El vendedor busca productos, los agrega al carrito, selecciona el medio de pago, que puede tener un descuento o recargo asociado, y presiona Confirmar Venta.

En ese momento, antes de guardar nada en la base de datos, aparece un modal de confirmacion con un ticket resumido: lista de items, cantidades, subtotales, medio de pago y monto total final. El vendedor puede revisar y confirmar, o cancelar si detecta un error. Esto evita ventas erroneas que luego requieren devoluciones.

El Dashboard es el panel de control para el duenio del negocio. Muestra tarjetas con metricas clave: ventas del dia, stock bajo, total de movimientos. Lo interesante es que cada tarjeta es expandible: al hacer clic, se despliega suavemente con una animacion CSS y muestra el detalle completo. Por ejemplo, la tarjeta de Stock Bajo muestra la tabla con todos los productos bajo el umbral minimo.

Todo el estilo usa modo oscuro con glassmorphism, ese efecto de vidrio que ven en pantalla, lo que le da una identidad visual moderna y profesional al sistema."

---

## SLIDE 12 - DESARROLLO ASISTIDO POR IA (~1 min)

[INT. 2:]
"Un aspecto diferencial del proceso de desarrollo fue el uso de inteligencia artificial como co-piloto. Utilizamos Antigravity, un asistente de IA de Google DeepMind, con un protocolo de trabajo estructurado por fases.

El flujo fue el siguiente: primero disenamos el modelo de datos, luego generamos el esquema SQL y los triggers, despues construimos el backend con FastAPI, luego el frontend con Jinja2 y Bootstrap, y finalmente integramos todo y corregimos errores.

En cada fase, el equipo tomo las decisiones tecnicas: que tablas crear, que restricciones aplicar, que consultas optimizar. Y la IA nos asistio en la implementacion y en detectar errores.

La IA acelera el desarrollo, pero no reemplaza el criterio tecnico. Cada linea de codigo que ven hoy fue revisada, entendida y validada por nosotros. El valor de la herramienta esta en cuanto la sabes usar, no en dejar que haga todo sola."

---

## SLIDE 13 - CONCLUSIONES Y CIERRE (~1 min)

[INT. 2:]
"Para cerrar, voy a resumir que logramos y que aprendimos.

Logramos construir un sistema de gestion funcional para una PYME real. Una base de datos en 3FN con 13 tablas, integridad garantizada por triggers y claves foraneas compuestas, consultas optimizadas con algebra relacional, y una interfaz moderna y usable.

En terminos de aprendizajes: la normalizacion no es un ejercicio teorico, evita bugs reales en produccion. Los triggers son la ultima linea de defensa de la integridad de datos. Elegir psycopg2 sobre un ORM nos obligo a pensar en SQL de verdad. Y trabajar con IA de forma estructurada es una habilidad del desarrollo moderno.

Estamos abiertos a preguntas. Muchas gracias."

---

# ===============================
# PARTE 3 - DETALLES TECNICOS CRITICOS
# ===============================

> Esta seccion es una referencia de profundizacion para responder preguntas del profesor.

---

## 3.1 - TRIGGERS: Detalle Tecnico Completo

### Trigger para Venta (Decremento de Stock)

```sql
CREATE OR REPLACE FUNCTION fn_actualizar_stock_venta()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id_variante = NEW.id_variante;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Variante % no encontrada', NEW.id_variante;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_venta
    AFTER INSERT ON detalle_venta
    FOR EACH ROW
    EXECUTE FUNCTION fn_actualizar_stock_venta();
```

### Trigger para Compra (Incremento de Stock)

```sql
CREATE OR REPLACE FUNCTION fn_actualizar_stock_compra()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE variante_producto
    SET stock_actual = stock_actual + NEW.cantidad
    WHERE id_variante = NEW.id_variante;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_compra
    AFTER INSERT ON detalle_compra
    FOR EACH ROW
    EXECUTE FUNCTION fn_actualizar_stock_compra();
```

Puntos clave:
- NEW es el registro recien insertado (accesible solo en triggers AFTER INSERT/UPDATE)
- FOR EACH ROW significa que el trigger se dispara por cada fila insertada
- El trigger opera DESPUES del INSERT (AFTER), garantizando que el dato ya fue persistido
- IF NOT FOUND es una guarda de seguridad adicional

---

## 3.2 - TABLA DEVOLUCION: FK Compuesta

```sql
CREATE TABLE detalle_venta (
    id_venta        INTEGER NOT NULL,
    renglon_venta   INTEGER NOT NULL,
    id_variante     INTEGER NOT NULL,
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_venta, renglon_venta),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (id_variante) REFERENCES variante_producto(id_variante)
);

CREATE TABLE devolucion (
    id_devolucion     SERIAL PRIMARY KEY,
    id_venta          INTEGER NOT NULL,
    renglon_venta     INTEGER NOT NULL,
    cantidad_devuelta INTEGER NOT NULL CHECK (cantidad_devuelta > 0),
    motivo            TEXT,
    fecha_devolucion  DATE DEFAULT CURRENT_DATE,

    CONSTRAINT fk_devolucion_detalle
        FOREIGN KEY (id_venta, renglon_venta)
        REFERENCES detalle_venta(id_venta, renglon_venta)
        ON DELETE RESTRICT
);
```

Comparacion de garantias:

| Escenario | FK Simple a id_venta | FK Compuesta (id_venta, renglon_venta) |
|---|---|---|
| Devolver item que SI estuvo en la venta | Permitido | Permitido |
| Devolver item que NO estuvo en la venta | Permitido (bug!) | Rechazado por la BD |
| Devolver item de otra venta | Permitido (bug!) | Rechazado por la BD |

---

## 3.3 - ALGEBRA RELACIONAL: Push-Down de Selecciones

### Consulta SQL de ejemplo

```sql
SELECT p.nombre, v.fecha, SUM(dv.cantidad) AS total_vendido
FROM venta v
JOIN detalle_venta dv ON v.id_venta = dv.id_venta
JOIN variante_producto vp ON dv.id_variante = vp.id_variante
JOIN producto p ON vp.id_producto = p.id_producto
WHERE v.fecha = CURRENT_DATE
GROUP BY p.nombre, v.fecha
ORDER BY total_vendido DESC;
```

### Arbol SIN optimizacion (ineficiente)

```
     pi (nombre, fecha, total_vendido)
                  |
         gamma GROUP BY (nombre, fecha)
                  |
        sigma (fecha = CURRENT_DATE)  <- Filtro al FINAL
                  |
            JOIN (id_producto)
           /               \
  variante_producto       producto
          |
    JOIN (id_variante)
   /              \
detalle_venta   variante_producto
      |
JOIN (id_venta)
/             \
venta      detalle_venta
```

Problema: se unen TODAS las ventas antes de filtrar por fecha.

### Arbol CON Push-Down (eficiente)

```
     pi (nombre, fecha, total_vendido)
                  |
         gamma GROUP BY (nombre, fecha)
                  |
            JOIN (id_producto)
           /               \
  variante_producto       producto
          |
    JOIN (id_variante)
   /              \
detalle_venta   variante_producto
      |
JOIN (id_venta)
/                           \
sigma (fecha=CURRENT_DATE)   detalle_venta
|
venta
```

El JOIN recibe solo las ventas de hoy -> tablas intermedias mucho mas pequenias.

Regla: Aplicar sigma (WHERE) tan cerca de las hojas del arbol como sea posible, antes de cualquier JOIN.

---

## 3.4 - POOL DE CONEXIONES: psycopg2 ThreadedConnectionPool

```python
from psycopg2 import pool

connection_pool = pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    dsn="postgresql://user:password@localhost/marroquineria"
)

def get_connection():
    conn = connection_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)
```

Beneficios:
- Evita el costo de abrir/cerrar una conexion TCP por cada request HTTP
- Permite multiples usuarios simultaneos sin conflictos
- ThreadedConnectionPool es thread-safe (seguro para uso concurrente)

---

## 3.5 - NORMALIZACION: Resumen de Formas Normales

| Forma Normal | Condicion | Cumplida |
|---|---|---|
| 1FN | Atributos atomicos, sin grupos repetitivos | Si |
| 2FN | Todo atributo no-clave depende de la PK completa | Si |
| 3FN | No hay dependencias transitivas | Si |
| BCNF | Toda dependencia funcional tiene superclave del lado izquierdo | Si (en la mayoria de tablas) |

Ejemplo de dependencia transitiva eliminada:

```
Sin 3FN: variante_producto(id_variante, id_categoria, nombre_categoria)
  -> id_variante -> id_categoria -> nombre_categoria [dependencia transitiva!]

Con 3FN:
  variante_producto(id_variante, id_categoria, ...)
  categoria(id_categoria, nombre_categoria)
```

---

## PREGUNTAS FRECUENTES DEL PROFESOR - Respuestas preparadas

P: iPor que no usaron BCNF en vez de 3FN?
R: "BCNF es mas restrictiva y en algunos casos obliga a descomponer tablas de forma que se pierden dependencias funcionales. 3FN es el estandar recomendado en diseno practico de bases de datos porque elimina las redundancias problematicas sin sacrificar la capacidad de reconstruir las dependencias funcionales originales."

P: iQue pasa si el trigger falla a mitad de una transaccion?
R: "Toda la transaccion se hace rollback. Si el INSERT en detalle_venta dispara el trigger y el UPDATE en variante_producto falla, PostgreSQL deshace automaticamente el INSERT tambien. El trigger corre dentro de la misma transaccion, es atomico."

P: iComo manejan la concurrencia? iDos vendedores pueden vender el ultimo item al mismo tiempo?
R: "Manejamos esto con bloqueos a nivel de fila en PostgreSQL. Al hacer el UPDATE en variante_producto dentro del trigger, PostgreSQL aplica un row-level lock. El segundo UPDATE espera hasta que el primero termine. Ademas, tenemos un CHECK que puede validar stock > 0 antes de confirmar."

P: iPor que eligieron FastAPI sobre Django o Flask?
R: "FastAPI tiene soporte nativo para async/await, documentacion automatica con Swagger, tipado con Pydantic, y es significativamente mas rapido que Flask. Para un sistema de gestion donde la velocidad de respuesta importa, es la eleccion mas moderna."

---

*Archivo generado para: Sistema de Gestion Integral para Marroquineria*
*Version: Presentacion Final - Bases de Datos*