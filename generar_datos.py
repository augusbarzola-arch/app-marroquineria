import random
import datetime

NUM_PRODUCTOS = 50
DIAS = 90
VENTAS_POR_DIA_MIN = 5
VENTAS_POR_DIA_MAX = 15
COMPRAS_POR_MES = 8
PROBABILIDAD_DEVOLUCION = 0.05
ARCHIVO_SALIDA = "data/datos_marroquineria.sql"

random.seed(42)

categorias = ["Bolsos", "Mochilas", "Carteras", "Billeteras", "Cinturones", "Riñoneras", "Valijas", "Fundas", "Estuches", "Morrales"]
materiales = ["Cuero vacuno", "Cuero sintético", "Lona", "Nylon", "Poliéster"]
colores = ["Negro", "Marrón", "Suela", "Rojo", "Azul", "Verde", "Beige", "Blanco", "Gris", "Único"]
talles = ["Único", "S", "M", "L", "XL"]

proveedores_base = [
    ("30-12345678-9", "Cueros del Sur S.A.", "11-4555-1234", "ventas@cuerosdelsur.com"),
    ("30-98765432-1", "Textiles del Oeste", "11-4555-5678", "info@textilesoeste.com"),
    ("30-11223344-5", "Accesorios Marro", "11-4555-9012", "contacto@accesoriosmarro.com"),
    ("30-55667788-0", "Distribuidora Central", "11-4555-3456", "pedidos@distcentral.com"),
    ("30-99887766-4", "Importadora Andina", "11-4555-7890", "ventas@importandina.com"),
    ("30-44332211-8", "Cuero y Diseño", "11-4555-2345", "hola@cueroydiseno.com"),
    ("30-77665544-2", "Marroquinería Mayorista", "11-4555-6789", "mayorista@marro.com"),
    ("30-33221100-6", "El Buen Cuero", "11-4555-0123", "info@elbuencuero.com"),
    ("30-66554433-0", "Suministros del Norte", "11-4555-4567", "norte@suministros.com"),
    ("30-22110099-4", "Global Leather", "11-4555-8901", "global@leather.com"),
]

medios_pago = [("Efectivo", -20.0), ("Transferencia", -20.0), ("Tarjeta Débito", 0.0), ("Tarjeta Crédito", 10.0)]
motivos_devolucion = ['CAMBIO', 'REPARACION', 'DEVOLUCION']

def esc(s): return str(s).replace("'", "''")
def sql_val(v):
    if v is None: return "NULL"
    if isinstance(v, str): return "'" + esc(v) + "'"
    if isinstance(v, datetime.datetime): return "'" + v.strftime('%Y-%m-%d %H:%M:%S') + "'"
    if isinstance(v, datetime.date): return "'" + v.strftime('%Y-%m-%d') + "'"
    return str(v)

def write_insert(f, tabla, columnas, filas):
    if not filas: return
    f.write(f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES\n")
    valores = ["(" + ", ".join([sql_val(v) for v in fila]) + ")" for fila in filas]
    f.write(",\n".join(valores) + ";\n\n")

print("Generando datos (Corregido)...")

categorias_data = [(i, n, f"Cat de {n}") for i, n in enumerate(categorias, 1)]
materiales_data = [(i, n) for i, n in enumerate(materiales, 1)]
colores_data = [(i, n) for i, n in enumerate(colores, 1)]
talles_data = [(i, n) for i, n in enumerate(talles, 1)]
proveedores_data = [(i, c, r, t, e) for i, (c, r, t, e) in enumerate(proveedores_base, 1)]
medios_pago_data = [(i, n, p) for i, (n, p) in enumerate(medios_pago, 1)]

productos_data = []
productos_dict = {}
for i in range(1, NUM_PRODUCTOS + 1):
    id_cat, id_mat = random.randint(1, 10), random.randint(1, 5)
    pc = round(random.uniform(1000, 8000), 2)
    pl = round(pc * random.uniform(1.5, 2.5), 2)
    productos_data.append((i, f"Producto {i} {random.choice(categorias)}", f"Desc {i}", pc, pl, id_cat, id_mat))
    productos_dict[i] = {"precio_costo": pc, "precio_lista": pl}

variantes_data = []
variantes_dict = {}
id_var = 1
for p in productos_data:
    combinaciones = set()
    for _ in range(random.randint(1, 4)):
        c, t = random.randint(1, 10), random.randint(1, 5)
        if (c, t) not in combinaciones:
            combinaciones.add((c, t))
            sa = random.randint(0, 100)
            variantes_data.append((id_var, p[0], c, t, sa, random.randint(5, 20)))
            variantes_dict[id_var] = {"id_producto": p[0], "precio_costo": p[3], "precio_lista": p[4]}
            id_var += 1

hoy = datetime.date.today()
fecha_inicio = hoy - datetime.timedelta(days=DIAS)
ventas_data, detalles_venta_data, detalles_por_venta = [], [], {}
id_venta, id_det = 1, 1

for dia in range(DIAS):
    fecha = fecha_inicio + datetime.timedelta(days=dia)
    for _ in range(random.randint(VENTAS_POR_DIA_MIN, VENTAS_POR_DIA_MAX)):
        fh = datetime.datetime(fecha.year, fecha.month, fecha.day, random.randint(9, 19), random.randint(0, 59))
        id_mp = random.randint(1, 4)
        num_items = random.randint(1, 4)
        detalles, monto = [], 0.0
        for _ in range(num_items):
            v = random.choice(list(variantes_dict.keys()))
            cant = random.randint(1, 3)
            pu = round(variantes_dict[v]["precio_lista"] * (1 + medios_pago[id_mp-1][1] / 100.0), 2)
            monto += cant * pu
            detalles.append((id_venta, id_det, cant, pu, v))
            id_det += 1
        ventas_data.append((id_venta, fh, round(monto, 2), id_mp))
        detalles_venta_data.extend(detalles)
        detalles_por_venta[id_venta] = detalles
        id_venta += 1

compras_data, detalles_compra_data = [], []
id_cmp, id_dcmp = 1, 1
for mes in range(3):
    for _ in range(COMPRAS_POR_MES):
        fc = datetime.date(fecha_inicio.year, fecha_inicio.month + mes if fecha_inicio.month + mes <= 12 else fecha_inicio.month + mes - 12, random.randint(1, 28))
        monto = 0.0
        for _ in range(random.randint(1, 5)):
            v = random.choice(list(variantes_dict.keys()))
            cant = random.randint(5, 20)
            pcu = variantes_dict[v]["precio_costo"]
            monto += cant * pcu
            detalles_compra_data.append((id_cmp, id_dcmp, cant, pcu, v))
            id_dcmp += 1
        compras_data.append((id_cmp, fc, round(monto, 2), random.randint(1, 10)))
        id_cmp += 1

devoluciones_data = []
id_dev = 1
for vta in ventas_data:
    if random.random() < PROBABILIDAD_DEVOLUCION and vta[0] in detalles_por_venta:
        det = random.choice(detalles_por_venta[vta[0]])
        cant_dev = random.randint(1, det[2])
        motivo = random.choice(motivos_devolucion)
        id_vn, mdif = None, 0.0
        
        if motivo == 'CAMBIO':
            prod_dev = variantes_dict[det[4]]["id_producto"]
            vars_mismo_prod = [v for v, info in variantes_dict.items() if info["id_producto"] == prod_dev and v != det[4]]
            if vars_mismo_prod:
                id_vn = random.choice(vars_mismo_prod)
                mdif = round((variantes_dict[id_vn]["precio_lista"] - det[3]) * cant_dev, 2)
            else:
                motivo = 'DEVOLUCION' # Si no hay otra variante, lo pasamos a devolucion
                
        devoluciones_data.append((id_dev, vta[1] + datetime.timedelta(days=random.randint(1, 15)), vta[0], det[1], cant_dev, motivo, id_vn, mdif, "Gen auto"))
        id_dev += 1

with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
    f.write("BEGIN;\n\n")
    write_insert(f, "CATEGORIA", ["id_categoria", "nombre_categoria", "descripcion"], categorias_data)
    write_insert(f, "MATERIAL", ["id_material", "nombre_material"], materiales_data)
    write_insert(f, "COLOR", ["id_color", "nombre_color"], colores_data)
    write_insert(f, "TAMANO", ["id_tamano", "nombre_tamano"], talles_data) # Ajustado a tamano por si acaso
    write_insert(f, "PROVEEDOR", ["id_proveedor", "cuit", "razon_social", "telefono", "email"], proveedores_data)
    write_insert(f, "MEDIO_PAGO", ["id_medio_pago", "nombre_medio", "porcentaje_descuento_recargo"], medios_pago_data)
    write_insert(f, "PRODUCTO", ["id_producto", "nombre_producto", "descripcion", "precio_costo", "precio_lista", "id_categoria", "id_material"], productos_data)
    write_insert(f, "VARIANTE_PRODUCTO", ["id_variante", "id_producto", "id_color", "id_talle", "stock_actual", "stock_minimo"], variantes_data)
    write_insert(f, "VENTA", ["id_venta", "fecha_hora", "monto_total", "id_medio_pago"], ventas_data)
    write_insert(f, "DETALLE_VENTA", ["id_venta", "renglon_venta", "cantidad", "precio_unitario_cobrado", "id_variante"], detalles_venta_data)
    write_insert(f, "COMPRA", ["id_compra", "fecha_compra", "monto_total", "id_proveedor"], compras_data)
    write_insert(f, "DETALLE_COMPRA", ["id_compra", "renglon_compra", "cantidad", "precio_costo_unitario", "id_variante"], detalles_compra_data)
    write_insert(f, "DEVOLUCION", ["id_devolucion", "fecha", "id_venta", "renglon_venta", "cantidad", "motivo", "id_variante_nueva", "monto_diferencia", "observaciones"], devoluciones_data)
    f.write("COMMIT;\n")
print("¡Archivo data/datos_marroquineria.sql generado!")