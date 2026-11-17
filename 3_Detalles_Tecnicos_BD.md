# PRESENTACION FINAL - SISTEMA DE GESTION PARA MARROQUINERIA
### Estructura de Diapositivas + Guion Hablado Completo

> **Formato:** PowerPoint / Google Slides
> **Duracion estimada:** 13-15 minutos
> **Integrantes:** 2 (Division equitativa)
> **Tono:** Profesional, academico, seguro y dinamico

---

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