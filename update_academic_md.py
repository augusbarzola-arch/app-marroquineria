import os

academic_md_content = """# 📋 ESTRUCTURA FORMAL DE DIAPOSITIVAS (13 SLIDES)
### Cátedra de Bases de Datos — Sistema de Gestión Comercial para Marroquinería
**Disertantes:** Augusto Barzola (Slides 1 a 7) & Lucas Duarte (Slides 8 a 13)

---

## 🖼️ SLIDE 1 — PORTADA
- **Título:** SISTEMA DE GESTIÓN PARA MARROQUINERÍA
- **Subtítulo:** Diseño Formal, Integridad y Optimización de una Base de Datos Relacional
- **Contexto:** Defensa de Proyecto Final — Cátedra de Bases de Datos
- **Autores:** Augusto Barzola (Slides 1 a 7) • Lucas Duarte (Slides 8 a 13)
- **Recurso Visual:** Diagrama DER relacional de fondo con esquema formal de entidades.

---

## 🖼️ SLIDE 2 — ÍNDICE TEMÁTICO (AGENDA ACADÉMICA)
- **Bloque I — Augusto Barzola (Modelado e Integridad):**
  1. Problemática del Dominio y Solución Relacional
  2. Arquitectura de Acceso a Datos y Flujo Transaccional
  3. Modelo Conceptual y DER (13 tablas relacionales)
  4. Teoría de Normalización: Demostración en 3FN
  5. Lógica Procedural en Motor: Triggers en PL/pgSQL
  6. Control Atómico de Inventario bajo Transacciones ACID
- **Bloque II — Lucas Duarte (Optimización y Consultas):**
  7. Integridad Referencial Avanzada: FK Compuesta en Devolución
  8. Consultas Complejas y Álgebra Relacional (Push-Down)
  9. Fundamentación Técnica: SQL Directo vs Abstracciones ORM
  10. Interfaz de Acceso a Datos como Cliente Transaccional
  11. Metodología de Diseño y Rol Asistencial de la IA
  12. Conclusiones Académicas y Defensa ante Preguntas de Cátedra

---

## 🖼️ SLIDE 3 — PROBLEMÁTICA DEL DOMINIO Y SOLUCIÓN RELACIONAL
- **Riesgos de Inconsistencia en el Dominio:**
  • Complejidad multidimensional: variantes ortogonales de material, color y tamaño por producto.
  • Anomalías de redundancia y actualización por registros desnormalizados.
  • Modificaciones concurrentes sin aislamiento ni control transaccional.
  • Devoluciones inconsistentes sin vínculo referencial con la venta original.
- **Garantías del Modelo Relacional:**
  • Esquema en PostgreSQL normalizado formalmente en 3FN.
  • Propiedades ACID garantizadas a nivel de motor en todas las operaciones.
  • Reglas de inventario gobernadas por Triggers procedurales en PL/pgSQL.
  • Integridad referencial blindada mediante claves foráneas compuestas.

---

## 🖼️ SLIDE 4 — ARQUITECTURA DE ACCESO A DATOS Y FLUJO TRANSACCIONAL
- **Componentes de la Arquitectura:**
  • Motor Relacional (PostgreSQL): Núcleo de persistencia, 13 tablas, restricciones CHECK, foreign keys y triggers en PL/pgSQL.
  • Capa de Servicios de Datos (FastAPI): API REST encargada del mapeo de datos y orquestación de transacciones hacia el motor.
  • Acceso Directo a Datos (psycopg2): Ejecución directa de SQL puro y parametrizado sin capas de abstracción ORM.
  • Interfaz de Acceso a Datos: Cliente visual que captura operaciones y emite transacciones hacia el motor para asegurar consistencia.
- **Recurso Visual:** Diagrama de capas mostrando el flujo transaccional directo hacia PostgreSQL.

---

## 🖼️ SLIDE 5 — MODELO DE DATOS — DER (13 TABLAS)
- **Entidades Fuertes / Maestras:** `producto`, `variante_producto`, `venta`, `compra`.
- **Entidades Débiles / Transaccionales:** `detalle_venta`, `detalle_compra`, `devolucion`.
- **Tablas de Dominio / Catálogo:** `categoria`, `material`, `color`, `tamano`, `proveedor`, `medio_pago`.
- **Rigor Relacional Aplicado:**
  • Claves primarias compuestas en entidades débiles: `(id_venta, renglon_venta)` y `(id_compra, renglon_compra)`.
  • Restricciones de integridad referencial: Cláusulas `ON DELETE RESTRICT` en todas las claves foráneas para evitar registros huérfanos.

---

## 🖼️ SLIDE 6 — NORMALIZACIÓN FORMAL EN TERCERA FORMA NORMAL (3FN)
- **1FN (Atributos Atómicos):** Cada columna almacena valores indivisibles; no existen arreglos ni grupos repetitivos.
- **2FN (Dependencia Completa):** En relaciones con clave compuesta (ej: `detalle_venta`), los atributos no-clave (precio, cantidad) dependen funcionalmente de la totalidad de la clave `(id_venta, renglon_venta)`.
- **3FN (Ausencia de Dependencia Transitiva):** Ningún atributo no-clave depende funcionalmente de otro atributo no-clave ($X \\to Y \\to Z$).
- **Demostración Práctica:**
  • *Sin 3FN:* `variante_producto(id_variante, color='Negro', material='Cuero')` → Dependencia transitiva $id\\_variante \\to color$.
  • *Con 3FN:* `variante_producto(id_variante, id_color, id_material)` y `color(id_color, nombre_color)` → Redundancia mínima, consistencia garantizada y actualización atómica en una única tupla.

---

## 🖼️ SLIDE 7 — LÓGICA PROCEDURAL EN MOTOR: TRIGGERS EN PL/PGSQL
- **Reglas de Negocio en Motor:**
  • El inventario se recalcula de forma ATÓMICA en el motor PostgreSQL.
  • `detalle_venta` (INSERT) → Trigger decrementa `stock_actual` en `variante_producto`.
  • `detalle_compra` (INSERT) → Trigger incrementa `stock_actual` al ingresar mercadería.
  • Independencia absoluta: el trigger se dispara ante cualquier canal de inserción (consola SQL, procesos batch o scripts externos).
  • Pseudorregistro `NEW` captura los atributos de la tupla entrante.
- **Definición Procedural:**
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

---

## 🖼️ SLIDE 8 — INTEGRIDAD REFERENCIAL: CLAVE FORÁNEA COMPUESTA EN DEVOLUCIÓN
- **Problema de Integridad a Resolver:**
  • ¿Cómo impedir en el motor la devolución de un ítem que nunca formó parte de la venta referenciada?
- **DDL Riguroso de la Tabla `devolucion`:**
```sql
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
- **Garantía Formal en el Motor:**
  • FK simple a `id_venta` permitiría registrar devoluciones de artículos inexistentes en ese comprobante.
  • FK compuesta sobre `(id_venta, renglon_venta)` obliga a la coincidencia simultánea con la línea vendida.
  • Rechazo determinístico: Si la tupla no existe, PostgreSQL aborta la transacción con error de integridad referencial.

---

## 🖼️ SLIDE 9 — CONSULTAS COMPLEJAS Y ÁLGEBRA RELACIONAL (PUSH-DOWN)
- **Árbol Canónico (Filtro Tardío — Ineficiente):**
  • $\\pi (\\text{nombre}, \\text{total\\_vendido}) \\leftarrow \\gamma (\\text{SUM}) \\leftarrow \\sigma (\\text{fecha}=\\text{HOY}) \\leftarrow \\bowtie (\\text{Todas las tablas})$.
  • Computa uniones sobre todo el histórico antes de filtrar por fecha, saturando la memoria temporal.
- **Árbol Optimizado con Push-Down de Selecciones:**
  • $\\pi (\\text{nombre}, \\text{total\\_vendido}) \\leftarrow \\gamma (\\text{SUM}) \\leftarrow \\bowtie \\leftarrow \\sigma (\\text{fecha}=\\text{HOY})(\\text{venta}) \\bowtie \\text{detalle\\_venta}$.
  • Selección $\\sigma$ descendida hasta la relación base `venta`.
  • Minimiza la cardinalidad de tuplas intermedias antes de cada JOIN, reduciendo el consumo de memoria de trabajo (`work_mem`) y acelerando el tiempo de procesamiento en el motor.

---

## 🖼️ SLIDE 10 — FUNDAMENTACIÓN TÉCNICA: SQL DIRECTO VS ORM
- **Desventajas de los ORM en Bases de Datos:**
  • Pérdida de control del plan de ejecución: sentencias SQL autogeneradas difíciles de predecir.
  • Ocultamiento del modelo relacional subyacente bajo capas opacas de objetos.
  • Dificultad en la gestión explícita de límites transaccionales.
  • Consultas analíticas complejas subóptimas.
- **Garantías de SQL Directo (psycopg2):**
  • Control absoluto de transacciones ACID: Delimitación explícita mediante bloques `BEGIN`, `COMMIT` y `ROLLBACK`.
  • Transparencia en el plan de ejecución: Visualización y afinamiento directo de consultas procesadas por el optimizador.
  • Uso de SQL parametrizado directo: Optimiza el reuso del plan de ejecución y neutraliza riesgos de inyección SQL.

---

## 🖼️ SLIDE 11 — INTERFAZ DE ACCESO A DATOS Y GESTIÓN DE TRANSACCIONES
- **Control Transaccional en Punto de Venta:**
  • Mecanismo de Verificación Previa al COMMIT: La interfaz consolida renglones, recargos y montos antes de emitir la transacción hacia PostgreSQL.
  • Previene transacciones erróneas en el motor que requerirían posteriores transacciones compensatorias (anulaciones o devoluciones).
  • Garantiza atomicidad en la inserción de cabecera y detalles.
- **Visualización de Consultas Analíticas:**
  • Consumo en tiempo real de consultas analíticas agregadas (`SUM`, `COUNT`, `GROUP BY`).
  • Visualización interactiva de saldos de inventario crítico y productos bajo stock mínimo.
  • Evidencia empírica de cómo una base de datos normalizada en 3FN soporta lecturas concurrentes sin bloqueos innecesarios.

---

## 🖼️ SLIDE 12 — METODOLOGÍA DE DISEÑO Y ROL ASISTENCIAL DE LA IA
- **Diseño Conceptual y Lógico Humano:**
  • El DER, la normalización en 3FN, las claves compuestas y las expresiones de álgebra relacional fueron concebidos, calculados y validados íntegramente por los autores.
- **Rol Acotado de la Inteligencia Artificial:**
  • La IA se empleó exclusivamente como un copiloto mecánico para agilizar el tipeo del código DDL extenso y el boilerplate de conexión.
  • Las decisiones de arquitectura de datos y la auditoría de integridad fueron ejecutadas 100% por el equipo.

---

## 🖼️ SLIDE 13 — CONCLUSIONES ACADÉMICAS Y CIERRE
- **Resultados del Modelo Relacional:**
  • Esquema de 13 tablas relacionales en 3FN libre de redundancias y anomalías.
  • Integridad protegida a nivel motor mediante triggers en PL/pgSQL y claves compuestas.
  • Optimización formal demostrable en álgebra relacional mediante la heurística de push-down.
  • Control transaccional estricto bajo el estándar SQL sin dependencias de ORMs.
- **Lecciones de la Disciplina:**
  • La robustez de los datos debe residir en el SGBD y no delegarse a la aplicación.
  • La normalización es un fundamento de ingeniería que previene inconsistencias críticas.
  • El análisis formal de consultas optimiza el uso de recursos y memoria en el motor.
"""

with open("1_Estructura_Diapositivas.md", "w", encoding="utf-8") as f:
    f.write(academic_md_content)

print("1_Estructura_Diapositivas.md updated successfully with academic focus!")
