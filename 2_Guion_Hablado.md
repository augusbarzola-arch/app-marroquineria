# 🎙️ GUION HABLADO OFICIAL — DEFENSA DE BASES DE DATOS (50% / 50%)
### Sistema de Gestión Comercial para Marroquinería
**Disertantes:** Augusto Barzola & Lucas Duarte  
**Duración total estimada:** 12 - 14 minutos (~6.5 minutos cada uno)  
**Tono:** Académico formal, riguroso, seguro y enfocado en SGBD

---

## 📊 TABLA DE DISTRIBUCIÓN EQUITATIVA (50% / 50%)

| Bloque | Disertante | Diapositivas | Ejes Conceptuales de Base de Datos | Tiempo |
|---|---|---|---|---|
| **PRIMERA MITAD** | **Augusto Barzola** | **Slides 1 a 7** (7 diapositivas) | • Contexto de Negocio y Dominio de Datos<br>• Agenda de Exposición Académica<br>• Justificación del Motor Relacional (ACID)<br>• Arquitectura de Acceso a Datos y Capas Transaccionales<br>• Modelo de Datos — DER (13 tablas relacionales)<br>• Teoría de Normalización (1FN, 2FN, 3FN)<br>• Triggers en PL/pgSQL y Reglas de Negocio en Motor | **~6.5 min** |
| **SEGUNDA MITAD** | **Lucas Duarte** | **Slides 8 a 13** (6 diapositivas) | • Integridad Referencial: FK Compuesta en Devolución<br>• Consultas Complejas y Álgebra Relacional (Push-Down)<br>• Fundamentación Técnica: SQL Directo vs ORM (ACID)<br>• Interfaz de Acceso a Datos como Cliente Transaccional<br>• Metodología de Diseño y Rol Asistencial de la IA<br>• Conclusiones Académicas y Preguntas de Cátedra | **~6.5 min** |

---

## DIAPOSITIVA 1: PORTADA — SISTEMA DE GESTIÓN PARA MARROQUINERÍA
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~30 seg

> "Buenos días profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy presentamos la defensa de nuestro proyecto final para la cátedra de Bases de Datos.
> 
> El proyecto aborda el diseño formal, la implementación y la optimización de una base de datos relacional orientada a la gestión comercial integral de una marroquinería, desarrollada sobre el motor PostgreSQL con una arquitectura de acceso a datos directa en Python.
> 
> El objetivo central de este desarrollo fue garantizar que la integridad referencial, el aislamiento transaccional y las reglas de negocio críticas residan estrictamente en el motor de base de datos, optimizando además el costo computacional de las consultas analíticas."

---

## DIAPOSITIVA 2: ÍNDICE TEMÁTICO — HOJA DE RUTA ACADÉMICA
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~30 seg

> "La exposición se encuentra dividida formalmente en dos bloques equitativos de 50%:
> 
> • En la primera mitad, abordaré la modelización conceptual y lógica: el problema del dominio de datos, la justificación de un motor ACID, el Diagrama Entidad-Relación de 13 tablas, la demostración formal de la Tercera Forma Normal (3FN) y la implementación de triggers en PL/pgSQL para la automatización atómica del inventario.
> 
> • En la segunda mitad, Lucas desarrollará la integridad referencial avanzada mediante claves foráneas compuestas en devoluciones, el modelado y optimización de consultas a través del Álgebra Relacional con push-down de selecciones, la justificación del uso de SQL directo sobre abstracciones ORM, la interacción de la interfaz consumidora y las conclusiones metodológicas."

---

## DIAPOSITIVA 3: PROBLEMÁTICA DEL DOMINIO Y SOLUCIÓN RELACIONAL
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~1 min

> "El negocio de una marroquinería presenta una complejidad representativa clásica: un mismo producto genérico se descompone en múltiples variantes según dimensiones ortogonales como material, color y tamaño.
> 
> La ausencia de un modelo estructurado genera los problemas clásicos de inconsistencia que estudiamos en la materia:
> 1. Anomalías de actualización: redundancia de información descriptiva en múltiples registros.
> 2. Inconsistencia de inventario: modificaciones concurrentes sin aislamiento ni actualización atómica.
> 3. Falta de integridad referencial: registros de devoluciones sin vínculo verificable con el comprobante de venta original.
> 
> Nuestra solución consistió en diseñar un esquema relacional normalizado en PostgreSQL donde el motor es la única fuente de verdad, aplicando restricciones declarativas y procedimentales para asegurar la integridad física y lógica de los datos."

---

## DIAPOSITIVA 4: ARQUITECTURA DE ACCESO A DATOS Y FLUJO TRANSACCIONAL
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~1 min

> "Desde el punto de vista arquitectónico, el sistema prioriza la pureza en el acceso al motor relacional:
> 
> 1. Motor Relacional (PostgreSQL): Es el núcleo del sistema. Aloja 13 tablas relacionales, constraints CHECK, restricciones de unicidad, claves foráneas compuestas y procedimientos almacenados ejecutados por triggers.
> 2. Capa de Servicios de Datos: Desarrollada en Python con FastAPI, actúa como intermediario para exponer los datos y orquestar transacciones explícitas.
> 3. Conexión Directa a Datos (psycopg2): Permite la ejecución de sentencias SQL puras y parametrizadas sin capas intermedias que desvirtúen el plan de ejecución.
> 4. Interfaz de Acceso a Datos: Actúa exclusivamente como un cliente consumidor que captura las operaciones del usuario y las transforma en transacciones ACID hacia la base de datos."

---

## DIAPOSITIVA 5: MODELO DE DATOS — DIAGRAMA ENTIDAD-RELACIÓN (13 TABLAS)
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~1.5 min

> "El modelo relacional consta de 13 tablas estructuradas para representar con exactitud el ciclo transaccional:
> 
> • Entidades Fuertes o Maestras: "producto", "variante_producto", "venta" y "compra", que constituyen el núcleo de la actividad del negocio.
> • Entidades Débiles y Transaccionales: "detalle_venta", "detalle_compra" y "devolucion", que registran los ítems granulares de cada transacción.
> • Tablas de Dominio o Catálogo: "categoria", "material", "color", "tamano", "proveedor" y "medio_pago", utilizadas para restringir dominios finitos de atributos.
> 
> Un aspecto crítico de diseño es el uso de Claves Primarias Compuestas en las entidades débiles, como (id_venta, renglon_venta), lo que formaliza la dependencia de existencia e identificación. Asimismo, todas las asociaciones cuentan con restricciones de clave foránea con cláusulas ON DELETE RESTRICT para evitar registros huérfanos."

---

## DIAPOSITIVA 6: NORMALIZACIÓN FORMAL EN TERCERA FORMA NORMAL (3FN)
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~1.5 min

> "Un eje central de evaluación es la normalización del esquema, el cual satisface estrictamente la Tercera Forma Normal (3FN):
> 
> • Primera Forma Normal (1FN): Todos los dominios de atributos son atómicos. No existen listas, arreglos ni grupos repetitivos dentro de una misma columna.
> • Segunda Forma Normal (2FN): Se encuentra en 1FN y cada atributo no primario posee dependencia funcional completa respecto a la clave primaria. En entidades compuestas como "detalle_venta", atributos como cantidad y precio unitario dependen de la totalidad de la clave (id_venta, renglon_venta) y no de una parte de ella.
> • Tercera Forma Normal (3FN): Se encuentra en 2FN y ningún atributo no-clave depende transitivamente de la clave primaria (X → Y → Z).
> 
> Demostración práctica: Si en "variante_producto" hubiésemos almacenado la descripción del color o material, tendríamos dependencias transitivas: id_variante determina id_color, y este determina nombre_color. Al aislar "color" en una relación independiente, eliminamos anomalías de inserción, actualización y borrado."

---

## DIAPOSITIVA 7: TRIGGERS EN PL/PGSQL: AUTOMATIZACIÓN EN EL MOTOR
- **Disertante:** Augusto Barzola
- **Tiempo sugerido:** ~1.5 min

> "Para garantizar que las reglas de negocio de inventario se cumplan sin depender de la aplicación, implementamos Triggers en PL/pgSQL directamente en el motor:
> 
> • Al producirse un evento INSERT sobre "detalle_venta", se dispara el trigger "trg_stock_venta", ejecutando una función que resta atómicamente el stock en "variante_producto" utilizando el pseudorregistro "NEW.cantidad".
> • De forma recíproca, al insertarse registros en "detalle_compra", el trigger correspondiente incrementa el stock disponible.
> 
> La relevancia académica de esta solución radica en que la regla de integridad de stock queda blindada en el motor. Si un operador ingresa información mediante consola SQL, procesos por lotes o scripts externos, el trigger se dispara indefectiblemente, garantizando consistencia transaccional absoluta.
> 
> [TRANSICIÓN]: Habiendo expuesto el modelo relacional, la normalización y la lógica procedural en el motor, le cedo la palabra a Lucas para abordar la integridad en devoluciones, el análisis de álgebra relacional y las consultas complejas."

---

## DIAPOSITIVA 8: TABLA DEVOLUCIÓN: INTEGRIDAD CON CLAVE FORÁNEA COMPUESTA
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~1.5 min

> "Gracias Augusto. Continuando con los aspectos críticos de integridad referencial, analizamos el diseño formal de la entidad "devolucion".
> 
> El problema teórico y práctico consistía en: ¿Cómo garantizar que no se pueda registrar una devolución de un producto que jamás formó parte de esa venta específica?
> 
> Si hubiésemos definido una clave foránea simple referenciando únicamente a "id_venta", el motor solo verificaría la existencia del comprobante cabecera, permitiendo registrar devoluciones inconsistentes o artículos ajenos al ticket.
> 
> La solución implementada fue definir una Clave Foránea Compuesta sobre (id_venta, renglon_venta) que referencia exactamente a la clave primaria de "detalle_venta". De esta manera, el motor valida de forma determinística la existencia física de la línea vendida. Si el par no existe en el detalle, PostgreSQL aborta la operación y rechaza el registro por violación de Foreign Key, garantizando integridad referencial estricta."

---

## DIAPOSITIVA 9: ÁLGEBRA RELACIONAL Y HEURÍSTICA DE PUSH-DOWN
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~2 min

> "Implementamos 6 consultas complejas con agrupaciones y uniones múltiples. Para evaluar formalmente la consulta de recaudación diaria por producto, modelamos su Árbol de Álgebra Relacional y analizamos su optimización:
> 
> • En el Árbol Canónico o No Optimizado, se computan sucesivamente las reuniones naturales (JOINs) de todas las tuplas históricas de "venta", "detalle_venta", "variante" y "producto", y recién en el nodo superior se aplica la selección sigma (fecha = fecha_actual). Esta aproximación es computacionalmente ineficiente debido a la gran cardinalidad de los conjuntos intermedios generados.
> 
> • En el Árbol Optimizado, aplicamos la heurística formal de Push-Down de Selecciones: conmutar el operador de selección sigma descendiéndolo a través del árbol hasta alcanzar la relación base "venta". Al filtrar las ventas del día previo a la operación de Join, la cardinalidad de tuplas intermedias se reduce en varios órdenes de magnitud, optimizando el uso de memoria de trabajo (work_mem) y reduciendo el tiempo de procesamiento en el motor."

---

## DIAPOSITIVA 10: FUNDAMENTACIÓN TÉCNICA: SQL DIRECTO VS ABSTRACCIONES ORM
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~1 min

> "Una decisión clave de arquitectura fue prescindir de un ORM y ejecutar sentencias SQL puras mediante psycopg2. Fundamentamos esta elección en principios propios de la disciplina:
> 
> 1. Control absoluto de transacciones ACID: Administramos de forma explícita los límites transaccionales mediante bloques BEGIN, COMMIT y ROLLBACK ante excepciones, asegurando atomicidad y durabilidad completas.
> 2. Transparencia en el plan de ejecución: Los ORM generan sentencias autogeneradas que a menudo ocultan planes subóptimos o lecturas anidadas indeseadas. Con SQL directo garantizamos visibilidad total del plan que procesa el optimizador.
> 3. Uso de SQL parametrizado directo: Empleamos paso de argumentos por parámetros para optimizar la reutilización del plan de ejecución en el motor y eliminar cualquier riesgo de inyección SQL."

---

## DIAPOSITIVA 11: INTERFAZ DE ACCESO A DATOS Y GESTIÓN DE TRANSACCIONES
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~1.5 min

> "Como valor agregado para la gestión operativa, desarrollamos una Interfaz de Acceso a Datos que funciona estrictamente como cliente de las transacciones del motor:
> 
> • En el Punto de Venta: Diseñamos un flujo de verificación previa. Antes de emitir el comando transaccional hacia PostgreSQL, el usuario visualiza una confirmación que consolida los ítems calculados. Esto previene el envío de transacciones erróneas que exigirían posteriores transacciones compensatorias de anulación o devolución en la base de datos.
> 
> • En el Módulo de Monitoreo: La interfaz consume consultas agregadas optimizadas que leen en tiempo real métricas de inventario crítico y ventas diarias, demostrando cómo una visualización clara depende directamente de una base de datos normalizada y consultas indexadas eficientes."

---

## DIAPOSITIVA 12: METODOLOGÍA DE DISEÑO Y ROL ASISTENCIAL DE LA IA
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~1 min

> "Respecto a la metodología de desarrollo, aplicamos un protocolo estructurado por fases donde la Inteligencia Artificial cumplió un rol secundario y acotado:
> 
> Queremos enfatizar que el diseño conceptual, la elaboración del Diagrama Entidad-Relación, la aplicación formal de la Tercera Forma Normal, la definición de claves compuestas y la formulación de expresiones de Álgebra Relacional fueron concebidos, calculados y validados íntegramente por nosotros como autores del proyecto.
> 
> La herramienta de IA actuó únicamente como un asistente mecánico de apoyo para agilizar el tipeo del código DDL extenso y el boilerplate de conexión, manteniendo el equipo el control técnico y decisional en cada etapa del desarrollo."

---

## DIAPOSITIVA 13: CONCLUSIONES ACADÉMICAS Y CIERRE
- **Disertante:** Lucas Duarte
- **Tiempo sugerido:** ~1 min

> "Para concluir la defensa del proyecto, destacamos las siguientes conclusiones técnicas:
> 
> 1. Demostramos que la robustez y consistencia de un sistema no debe depender del software de aplicación, sino de las garantías formales que provee el motor relacional mediante esquemas normalizados, triggers y constraints de clave foránea compuesta.
> 2. La normalización en 3FN y las técnicas de optimización en Álgebra Relacional como el push-down de selecciones no son conceptos teóricos abstractos, sino fundamentos de ingeniería indispensables para el rendimiento y la escalabilidad de bases de datos relacionales.
> 3. El control explícito sobre las transacciones y consultas garantiza previsibilidad y rigor en el comportamiento del sistema.
> 
> Agradecemos a la cátedra por su atención y quedamos a su entera disposición para responder las preguntas sobre el proyecto."

---
