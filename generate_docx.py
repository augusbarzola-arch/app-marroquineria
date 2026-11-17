import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_guion_docx():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles & Colors
    # Primary title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("GUION OFICIAL DE LA PRESENTACIÓN")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Sistema de Gestión Integral para Marroquinería — Proyecto Bases de Datos")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("Disertantes: Augusto Barzola & Lucas Duarte\nDuración estimada: 12 - 15 minutos | Modalidad: Presentación Final Universitaria\n")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(11)
    run_meta.font.bold = True
    run_meta.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Table of Distribution
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Integrante"
    hdr_cells[1].text = "Temas a Cargo"
    hdr_cells[2].text = "Diapositivas"

    for cell in hdr_cells:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    data = [
        ("Augusto Barzola", "Intro, Problema/Solución, DER (13 tablas), Normalización en 3FN, Triggers de Stock, Integridad en Devoluciones (FK compuesta), Álgebra Relacional (Push-Down) y SQL directo vs ORM.", "Slides 1, 2, 3, 5, 6, 7, 8, 9, 10"),
        ("Lucas Duarte", "Arquitectura del Sistema (Stack FastAPI + psycopg2 + Jinja2), Demo UI/UX (Modal Ticket POS y Dashboard con tarjetas expandibles), Desarrollo asistido con IA, Conclusiones y Cierre.", "Slides 4, 11, 12, 13")
    ]

    for row_data in data:
        row = table.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            shd_col = "F1F5F9" if row_data[0] == "Augusto Barzola" else "EEF2FF"
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shd_col}"/>')
            cell._tc.get_or_add_tcPr().append(shd)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Scripts for each slide
    slides = [
        (
            1, "PORTADA", "Augusto Barzola", "~30 seg",
            'Buenos días / buenas tardes profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy les vamos a presentar nuestro proyecto final para la materia Bases de Datos.\n\nEl proyecto se titula "Sistema de Gestión Integral para Marroquinería": un desarrollo Full Stack concebido desde el modelado relacional riguroso en PostgreSQL, un backend en Python con FastAPI y psycopg2, y una interfaz web con experiencia de usuario moderna.\n\nEn los próximos minutos vamos a recorrer las decisiones de arquitectura, los desafíos de integridad y cómo optimizamos las consultas complejas.'
        ),
        (
            2, "ÍNDICE / AGENDA", "Augusto Barzola", "~30 seg",
            'Esta es la hoja de ruta de la presentación. Vamos a partir del problema real de negocio de una marroquinería y recorreremos los aspectos centrales evaluados por la cátedra:\n\n• Modelo de datos en Tercera Forma Normal (3FN).\n• Triggers de actualización atómica de inventario.\n• Garantía de integridad en devoluciones con clave foránea compuesta.\n• Optimización formal de consultas con Álgebra Relacional y Push-Down.\n• Justificación técnica de SQL puro frente a un ORM.\n• Demostración de interfaz y conclusiones.\n\nDividimos la exposición de forma equitativa: yo cubriré la base de datos, normalización y optimización matemática; y Lucas abordará la arquitectura de software, la interfaz de usuario y las conclusiones.'
        ),
        (
            3, "DESCRIPCIÓN DEL PROBLEMA Y SOLUCIÓN", "Augusto Barzola", "~1 min",
            'Para contextualizar el negocio: una marroquinería comercializa carteras, mochilas, cinturones y billeteras. Su complejidad principal radica en que cada producto cuenta con múltiples variantes: combinaciones de colores, materiales y tamaños.\n\nEn la PYME promedio, este control se lleva en cuadernos o planillas de cálculo descentralizadas, derivando en:\n1. Descuadres crónicos de inventario.\n2. Devoluciones inconsistentes que alteran la contabilidad.\n3. Nula visibilidad en tiempo real de recaudación y productos bajo stock de seguridad.\n\nNuestra respuesta fue un Sistema de Gestión Integral donde la base de datos es la única fuente de verdad: el motor protege su propia integridad mediante triggers y restricciones estrictas, brindándole al comerciante un Punto de Venta ágil y un Dashboard analítico en vivo.'
        ),
        (
            4, "ARQUITECTURA DEL SISTEMA — STACK TECNOLÓGICO", "Lucas Duarte", "~1.5 min",
            'TRANSICIÓN: [Augusto cede la palabra: "Para entender la ingeniería detrás del software, le paso la palabra a Lucas, quien explicará la arquitectura del sistema."]\n\nGracias Augusto.\n\nEl sistema fue estructurado bajo una arquitectura por capas desacoplada y eficiente:\n\n1. En la base del stack tenemos PostgreSQL, el motor relacional que almacena las 13 tablas normalizadas, las funciones PL/pgSQL y los triggers.\n2. En la capa de backend implementamos FastAPI con Python 3.11. Lo elegimos por su asincronismo nativo, su rendimiento superior y su tipado estricto.\n3. Para la persistencia no usamos un ORM: nos comunicamos de forma directa con psycopg2 mediante un ThreadedConnectionPool, garantizando transacciones atómicas y control total.\n4. En la presentación utilizamos Jinja2 para renderizado en servidor y Bootstrap 5 con JavaScript vanilla, logrando una interfaz en modo oscuro con estética Glassmorphism, limpia y responsiva.\n\nEs una arquitectura pensada para ser robusta sin introducir capas de abstracción innecesarias.'
        ),
        (
            5, "MODELO DE DATOS — DIAGRAMA ENTIDAD-RELACIÓN", "Augusto Barzola", "~1.5 min",
            'TRANSICIÓN: [Lucas devuelve: "Habiendo visto la arquitectura técnica, le devuelvo la palabra a Augusto para adentrarnos en el modelo relacional."]\n\nGracias Lucas. El modelo relacional consta de 13 tablas perfectamente articuladas en tres categorías:\n\n• Entidades maestras: producto, variante_producto, venta y compra.\n• Tablas transaccionales de detalle: detalle_venta, detalle_compra y devolucion.\n• Tablas de dominio o catálogo: categoria, material, color, tamano, proveedor y medio_pago.\n\nUn rasgo distintivo de nuestro diseño es el uso de Claves Primarias Compuestas en las tablas de detalle, como (id_venta, renglon_venta). Esto garantiza formalmente que cada renglón de un comprobante sea unívoco e irrepetible. Cada relación está protegida por Foreign Keys con cláusulas restrictivas que impiden la existencia de registros huérfanos.'
        ),
        (
            6, "NORMALIZACIÓN EN TERCERA FORMA NORMAL (3FN)", "Augusto Barzola", "~1.5 min",
            'Uno de los pilares evaluados por la cátedra es la normalización. El esquema cumple rigurosamente con la Tercera Forma Normal (3FN):\n\n• 1FN: Todos los atributos son atómicos y no existen grupos repetitivos.\n• 2FN: En las tablas con clave compuesta, los atributos dependen de la totalidad de la clave (no hay dependencias parciales).\n• 3FN: Erradicamos todas las dependencias transitivas; ningún atributo no-clave depende funcionalmente de otro atributo no-clave.\n\nEjemplo práctico: en lugar de guardar el nombre del color como texto en variante_producto —lo que provocaría anomalías de actualización y redundancia masiva— creamos la tabla satélite "color" y relacionamos únicamente su ID. Si el negocio decide renombrar un color, se ejecuta un único UPDATE en una sola fila, preservando la integridad del historial.'
        ),
        (
            7, "TRIGGERS DE STOCK: LA BASE DE DATOS SE PROTEGE A SÍ MISMA", "Augusto Barzola", "~2 min",
            'Pasamos a uno de los puntos técnicos centrales: los Triggers.\n\nEn nuestro sistema, la actualización del inventario NO se confía al backend ni a la aplicación web. El motor PostgreSQL se encarga de protegerse a sí mismo de manera automática:\n\n• Cada vez que se produce un INSERT en detalle_venta, el trigger trg_stock_venta dispara una función PL/pgSQL que decrementa automáticamente el stock_actual en variante_producto en la cantidad vendida.\n• De forma análoga, al registrar una compra en detalle_compra, otro trigger suma la cantidad al inventario.\n\n¿Por qué es fundamental esta decisión? Porque si un administrador carga datos directamente por consola con pgAdmin, o si se ejecuta un script de migración masiva, los triggers se activan invariablemente. En la función PL/pgSQL utilizamos la variable especial NEW.cantidad para leer el valor exacto del renglón recién insertado.'
        ),
        (
            8, "TABLA DEVOLUCIÓN: INTEGRIDAD CON CLAVE FORÁNEA COMPUESTA", "Augusto Barzola", "~1.5 min",
            'Un desafío clásico en sistemas comerciales es el tratamiento de las devoluciones. ¿Cómo garantizar que no se devuelva mercadería que nunca formó parte de esa venta?\n\nSi hubiésemos colocado una Foreign Key simple apuntando a id_venta, la base de datos únicamente validaría que la venta existió, permitiendo devolver cualquier producto ficticio.\n\nNuestra solución de ingeniería fue establecer una Clave Foránea Compuesta que referencia al par (id_venta, renglon_venta) de la tabla detalle_venta. Al intentar insertar una devolución, el motor valida obligatoriamente que dicho renglón exacto haya sido vendido en ese ticket. Si no existe, la base aborta la transacción y rechaza el registro físicamente.'
        ),
        (
            9, "CONSULTAS COMPLEJAS Y ÁLGEBRA RELACIONAL (PUSH-DOWN)", "Augusto Barzola", "~2 min",
            'Implementamos 6 consultas SQL complejas con subconsultas, agregaciones SUM y múltiples JOINs. Para analizar formalmente el plan de ejecución de una de las más demandantes —la recaudación del día agrupada por producto— modelamos el Árbol de Álgebra Relacional.\n\nUn árbol ingenuo realiza primero el producto cartesiano o JOINs de todas las ventas históricas, todos los detalles y todas las variantes, para recién al final aplicar la selección sigma (fecha = hoy). Esto satura la memoria con miles de registros intermedios innecesarios.\n\nAplicamos la heurística formal de Push-Down de Selecciones: empujar el operador de filtro sigma lo más cerca posible de las hojas del árbol. Al filtrar venta por fecha = hoy ANTES del JOIN, el operador de unión trabaja únicamente con las 20 transacciones del día. Esto reduce drásticamente el consumo de CPU y memoria temporal en el motor.'
        ),
        (
            10, "SQL DIRECTO CON PSYCOPG2 VS ORM", "Augusto Barzola", "~1 min",
            'Para cerrar el bloque de base de datos, justifico nuestra decisión de no usar un ORM:\n\nLibrerías como SQLAlchemy o Django ORM introducen capas opacas que suelen generar el problema de consultas N+1 y ocultan el control fino de transacciones.\n\nAl utilizar psycopg2 puro:\n1. Escribimos y optimizamos manualmente cada sentencia SQL.\n2. Administramos las transacciones con BEGIN, COMMIT y ROLLBACK explícitos ante excepciones.\n3. Implementamos un ThreadedConnectionPool que reutiliza conexiones abiertas de forma segura entre múltiples usuarios concurrentes.\n4. Para una cátedra universitaria, demostramos dominio absoluto del estándar SQL y del motor relacional.'
        ),
        (
            11, "INTERFAZ DE USUARIO: POS Y DASHBOARD", "Lucas Duarte", "~1.5 min",
            'TRANSICIÓN: [Augusto cede la palabra: "Con eso concluyo el análisis de la base de datos. Le paso la palabra a Lucas para recorrer la experiencia de usuario del sistema."]\n\nGracias Augusto.\n\nDiseñamos la interfaz enfocándonos en la velocidad operativa y la prevención activa de errores:\n\n• En el Punto de Venta (POS): el vendedor busca productos reactivamente, filtra por variante y selecciona el medio de pago, calculando descuentos o recargos al instante. Antes de impactar la base de datos, incorporamos un Modal de Confirmación con estética de ticket fiscal. El usuario revisa ítems, cantidades y totales antes de disparar el commit real, eliminando errores de facturación.\n\n• En el Dashboard Gerencial: presentamos tarjetas con métricas en tiempo real. Lo más interesante es que son Tarjetas Expandibles interactivas: al hacer clic en "Stock Bajo", la tarjeta se despliega suavemente y muestra la tabla completa de variantes bajo el umbral mínimo de seguridad. Todo bajo un diseño Glassmorphism en modo oscuro pensado para reducir la fatiga visual.'
        ),
        (
            12, "DESARROLLO ASISTIDO POR IA — PROTOCOLO POR FASES", "Lucas Duarte", "~1 min",
            'Un aspecto innovador de nuestra metodología fue incorporar herramientas de Inteligencia Artificial de vanguardia: utilizamos Antigravity de Google DeepMind bajo un estricto protocolo por fases:\n\n• Fase 1: Diseño conceptual y normalización del DER.\n• Fase 2: Construcción del DDL y triggers PL/pgSQL.\n• Fase 3: Lógica de endpoints en FastAPI y conexión psycopg2.\n• Fase 4: Interfaces en Jinja2 con modales y animaciones CSS.\n• Fase 5: Auditoría de integridad, optimización y depuración.\n\nQueremos enfatizar que la IA operó como un co-piloto técnico: aceleró la escritura de código base, pero las decisiones de arquitectura, el diseño relacional y la validación de cada línea fueron guiadas y auditadas íntegramente por nosotros.'
        ),
        (
            13, "CONCLUSIONES Y LECCIONES APRENDIDAS", "Lucas Duarte", "~1 min",
            'Para concluir, queremos sintetizar los logros y aprendizajes de este proyecto:\n\n1. Entregamos un software Full Stack completamente operativo para resolver una problemática comercial real.\n2. La base de datos es robusta, normalizada en 3FN y autosuficiente gracias a sus triggers y claves foráneas compuestas.\n3. Aprendimos que la normalización y el álgebra relacional no son meros conceptos teóricos de examen, sino herramientas indispensables para construir software escalable y libre de fallas.\n4. El control explícito sobre la base de datos supera ampliamente la delegación a ciegas en herramientas automatizadas.\n\nLes agradecemos su atención y quedamos a disposición de la cátedra para responder sus preguntas.'
        )
    ]

    for num, title, speaker, timing, text in slides:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        run_h = h.add_run(f"DIAPOSITIVA {num}: {title}")
        run_h.font.name = "Arial"
        run_h.font.size = Pt(13)
        run_h.font.bold = True
        run_h.font.color.rgb = RGBColor(15, 23, 42)

        p_info = doc.add_paragraph()
        p_info.paragraph_format.space_after = Pt(6)
        run_spk = p_info.add_run(f"Disertante: {speaker}  |  Tiempo sugerido: {timing}")
        run_spk.font.name = "Arial"
        run_spk.font.size = Pt(10)
        run_spk.font.bold = True
        col = RGBColor(2, 132, 199) if speaker == "Augusto Barzola" else RGBColor(124, 58, 237)
        run_spk.font.color.rgb = col

        p_text = doc.add_paragraph()
        p_text.paragraph_format.space_after = Pt(10)
        p_text.paragraph_format.line_spacing = 1.15
        run_t = p_text.add_run(text)
        run_t.font.name = "Arial"
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = RGBColor(30, 41, 59)

        # Divider
        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_after = Pt(8)
        run_div = p_div.add_run("―" * 50)
        run_div.font.color.rgb = RGBColor(203, 213, 225)

    doc_path = "Guion_Presentacion_Augusto_y_Lucas.docx"
    doc.save(doc_path)
    print(f"Document created successfully: {doc_path}")

if __name__ == "__main__":
    create_guion_docx()
