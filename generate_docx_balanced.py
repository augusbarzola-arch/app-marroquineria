import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_balanced_docx():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Titulo Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("GUION OFICIAL DE PRESENTACIÓN (DIVISIÓN 50/50)")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(20)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_s = p_sub.add_run("Sistema de Gestión Integral para Marroquinería — Proyecto Bases de Datos")
    run_s.font.name = "Arial"
    run_s.font.size = Pt(12)
    run_s.font.color.rgb = RGBColor(71, 85, 105)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_m = p_meta.add_run("Disertantes: Augusto Barzola & Lucas Duarte\nDuración estimada: 12 - 14 minutos (6-7 min por integrante) | Tono: Académico y Profesional\n")
    run_m.font.name = "Arial"
    run_m.font.size = Pt(10.5)
    run_m.font.bold = True
    run_m.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Tabla de División 50/50
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].text = "Disertante"
    hdr[1].text = "Diapositivas"
    hdr[2].text = "Temas a Cargo"
    hdr[3].text = "Tiempo"

    for cell in hdr:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    div_data = [
        ("PRIMERA MITAD\nAugusto Barzola", "Slides 1 a 7\n(7 diapositivas)", "• Portada y bienvenida\n• Agenda\n• Problema y Solución\n• Arquitectura del Sistema (Stack)\n• Modelo de Datos — DER (13 tablas)\n• Normalización en 3FN\n• Triggers de Stock (PL/pgSQL)", "~6.5 min"),
        ("SEGUNDA MITAD\nLucas Duarte", "Slides 8 a 13\n(6 diapositivas)", "• Tabla Devolución (FK compuesta)\n• Álgebra Relacional (Push-Down)\n• SQL directo (psycopg2) vs ORM\n• Demo UI/UX (POS Modal y Dashboard)\n• Metodología de desarrollo con IA\n• Conclusiones y preguntas", "~6.5 min")
    ]

    for row_info in div_data:
        r = table.add_row()
        for idx, val in enumerate(row_info):
            c = r.cells[idx]
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(9.5)
            shd_col = "F1F5F9" if "Augusto" in row_info[0] else "EEF2FF"
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shd_col}"/>')
            c._tc.get_or_add_tcPr().append(shd)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Contenido detallado
    slides_content = [
        (
            1, "PORTADA", "Augusto Barzola", "~30 seg",
            'Buenos días / buenas tardes profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy les vamos a presentar nuestro proyecto final para la materia Bases de Datos.\n\nEl sistema se titula "Sistema de Gestión Integral para Marroquinería": una solución Full Stack construida desde el diseño formal relacional en PostgreSQL, backend en Python con FastAPI y psycopg2, y una interfaz web moderna en modo oscuro con glassmorphism.\n\nEn los próximos minutos vamos a mostrar cómo la base de datos garantiza por sí misma la integridad del negocio y cómo optimizamos las consultas más exigentes.'
        ),
        (
            2, "ÍNDICE / AGENDA", "Augusto Barzola", "~30 seg",
            'Esta es la estructura de nuestra presentación:\n\n• Primero, analizaremos el problema del comercio y la solución que implementamos.\n• Luego, la arquitectura del sistema y el modelo de datos con sus 13 tablas normalizadas en 3FN.\n• Veremos los triggers de stock en PostgreSQL.\n• Después, Lucas explicará la integridad en devoluciones con clave foránea compuesta, la optimización matemática con Álgebra Relacional y por qué elegimos SQL directo sobre un ORM.\n• Y finalmente, recorreremos la interfaz de usuario, la metodología de desarrollo con IA y las conclusiones.\n\nDividimos la presentación en dos bloques continuos para que sea dinámica y clara.'
        ),
        (
            3, "DESCRIPCIÓN DEL PROBLEMA Y SOLUCIÓN", "Augusto Barzola", "~1 min",
            'Para contextualizar el negocio: una marroquinería vende artículos de cuero como carteras, mochilas, cinturones y billeteras. Su principal desafío operativo es que cada producto se diversifica en múltiples variantes según color, material y tamaño.\n\nEn la mayoría de las PYMEs, esta gestión se hace en cuadernos o planillas de Excel desarticuladas, lo que ocasiona:\n1. Descuadres constantes de inventario y roturas de stock no detectadas.\n2. Devoluciones sin comprobación estricta que provocan errores contables.\n3. Falta total de información en tiempo real sobre ventas diarias y productos críticos.\n\nNuestra solución fue desarrollar un Sistema de Gestión Integral centralizado en PostgreSQL, donde la base de datos opera como la única fuente de verdad: el motor protege su propia información con triggers y restricciones, brindándole al comerciante un Punto de Venta ágil y un Dashboard analítico en vivo.'
        ),
        (
            4, "ARQUITECTURA DEL SISTEMA — STACK TECNOLÓGICO", "Augusto Barzola", "~1 min",
            'La arquitectura del sistema sigue un modelo por capas limpio, robusto y desacoplado:\n\n1. En la base tenemos PostgreSQL: nuestro motor relacional ACID, donde residen las 13 tablas, las foreign keys, los constraints y los triggers en PL/pgSQL.\n2. En la capa de backend utilizamos Python con FastAPI. Lo seleccionamos por su velocidad asíncrona, bajo consumo de recursos y validación estricta de esquemas.\n3. Para la conexión a la base de datos optamos por psycopg2 directo con un ThreadedConnectionPool, permitiendo transacciones explícitas sin la sobrecarga de un ORM.\n4. Y en la capa de presentación usamos Jinja2 para renderizado en servidor junto a Bootstrap 5 y JavaScript vanilla, logrando una interfaz en modo oscuro con efecto glassmorphism, moderna y muy fluida.\n\nEs una estructura simple y confiable, sin capas intermedias innecesarias.'
        ),
        (
            5, "MODELO DE DATOS — DIAGRAMA ENTIDAD-RELACIÓN", "Augusto Barzola", "~1.5 min",
            'El modelo relacional está compuesto por 13 tablas organizadas en tres categorías bien definidas:\n\n• Entidades maestras: producto, variante_producto, venta y compra. Constituyen el núcleo transaccional del negocio.\n• Tablas de detalle: detalle_venta, detalle_compra y devolucion. Representan los ítems individuales de cada operación.\n• Tablas de dominio o catálogo: categoria, material, color, tamano, proveedor y medio_pago.\n\nUn punto de rigor técnico clave es que las tablas de detalle utilizan Claves Primarias Compuestas, como (id_venta, renglon_venta). Esto garantiza matemáticamente que dentro de un mismo comprobante cada renglón es único e irrepetible. Además, todas las relaciones cuentan con Foreign Keys que previenen registros huérfanos.'
        ),
        (
            6, "NORMALIZACIÓN EN TERCERA FORMA NORMAL (3FN)", "Augusto Barzola", "~1.5 min",
            'Un requisito central de la cátedra es la normalización. Nuestro esquema cumple rigurosamente con la Tercera Forma Normal (3FN):\n\n• Primera Forma Normal (1FN): Todos los atributos son atómicos y no existen grupos repetitivos ni arrays dentro de las columnas.\n• Segunda Forma Normal (2FN): En tablas con clave compuesta, los atributos dependen de la clave primaria completa y no de una parte de ella.\n• Tercera Forma Normal (3FN): No existen dependencias transitivas. Ningún atributo no-clave depende funcionalmente de otro atributo no-clave.\n\nEjemplo práctico: en lugar de guardar el color o el material como texto en la tabla variante_producto —lo que provocaría anomalías de actualización y duplicación de datos— creamos tablas independientes para color y material, referenciadas únicamente por su ID. Si se modifica un nombre, se realiza un solo UPDATE en una sola fila, garantizando consistencia absoluta en el historial.'
        ),
        (
            7, "TRIGGERS DE STOCK: LA BASE DE DATOS SE PROTEGE A SÍ MISMA", "Augusto Barzola", "~1.5 min",
            'Para cerrar mi bloque, quiero explicar uno de los puntos más relevantes del sistema: los Triggers en PostgreSQL.\n\nEn nuestra arquitectura, el control de inventario NO se delega a la aplicación ni al frontend. La base de datos se protege a sí misma de forma autónoma:\n\n• Al realizarse un INSERT en detalle_venta, el trigger trg_stock_venta dispara una función en PL/pgSQL que decrementa automáticamente el stock_actual de esa variante.\n• De forma inversa, al registrarse un INSERT en detalle_compra, otro trigger incrementa el stock al recibir mercadería del proveedor.\n\n¿Por qué es crucial? Porque si alguien inserta registros directamente desde pgAdmin, o mediante un script de importación, el trigger se ejecuta exactamente igual. La integridad del inventario no depende del canal de entrada. En el código PL/pgSQL utilizamos la variable especial NEW.cantidad para capturar el valor exacto del renglón recién insertado.\n\n[TRANSICIÓN CLAVE]: Habiendo visto la base de datos y sus triggers, le paso la palabra a Lucas, quien continuará con la integridad en devoluciones, el álgebra relacional, la interfaz y las conclusiones.'
        ),
        (
            8, "TABLA DEVOLUCIÓN: INTEGRIDAD CON CLAVE FORÁNEA COMPUESTA", "Lucas Duarte", "~1.5 min",
            'Gracias Augusto. Continuando con la solidez de la base de datos, quiero destacar el diseño de la tabla devolucion, que resuelve un problema crítico de integridad que una foreign key simple no puede solucionar.\n\nEl problema es: ¿cómo evitamos que se devuelva un ítem o producto que jamás formó parte de esa venta?\n\nSi hubiéramos usado una clave foránea simple apuntando a id_venta, la base de datos solo verificaría que la venta existió, pero permitiría registrar la devolución de cualquier producto ficticio o de otra venta.\n\nNuestra solución fue definir una Clave Foránea Compuesta que referencia directamente al par (id_venta, renglon_venta) de detalle_venta. De este modo, el motor valida obligatoriamente que ese renglón exacto haya sido vendido en ese ticket. Si no existe, PostgreSQL rechaza físicamente el INSERT con un error de integridad referencial. Es una garantía a nivel motor, sin depender de validaciones manuales de software.'
        ),
        (
            9, "CONSULTAS COMPLEJAS Y ÁLGEBRA RELACIONAL (PUSH-DOWN)", "Lucas Duarte", "~2 min",
            'Otro aspecto fundamental que evaluó la cátedra fueron las Consultas Complejas y el Álgebra Relacional. Desarrollamos 6 consultas analíticas con múltiples JOINs y agregaciones.\n\nPara optimizar la consulta más costosa —que calcula la recaudación del día agrupada por producto uniendo venta, detalle_venta, variante y producto— modelamos su Árbol de Álgebra Relacional.\n\nUn árbol ingenuo une primero todas las ventas históricas con todos los detalles y variantes, generando una tabla intermedia inmensa, para recién al final aplicar el filtro de fecha. Esto consume memoria innecesaria y ralentiza el motor.\n\nNosotros aplicamos formalmente la técnica de Push-Down de Selecciones: empujar el operador de filtro sigma (fecha = hoy) hacia las hojas del árbol, antes de realizar los JOINs. Al filtrar las ventas del día primero, el operador JOIN procesa únicamente los 20 comprobantes de hoy en vez de miles de registros históricos. Esta reducción drástica del conjunto intermedio es el principio de optimización que usan los motores de bases de datos profesionales.'
        ),
        (
            10, "SQL DIRECTO CON PSYCOPG2 VS ORM", "Lucas Duarte", "~1 min",
            'Una decisión arquitectónica importante que tomamos fue prescindir de un ORM y utilizar psycopg2 de forma directa.\n\nAunque herramientas como SQLAlchemy facilitan el prototipado rápido, introducen capas de abstracción opacas, generan consultas N+1 difíciles de predecir y complican el control fino de transacciones.\n\nAl trabajar con SQL puro y psycopg2:\n1. Escribimos y optimizamos cada consulta a mano con pleno control del plan de ejecución.\n2. Administramos transacciones explícitas con bloques BEGIN, COMMIT y ROLLBACK ante cualquier excepción.\n3. Implementamos un ThreadedConnectionPool que gestiona de 2 a 10 conexiones seguras para usuarios concurrentes.\n4. Y académicamente, demostramos dominio del lenguaje SQL estándar y de las capacidades nativas de PostgreSQL.'
        ),
        (
            11, "INTERFAZ DE USUARIO: POS Y DASHBOARD", "Lucas Duarte", "~1.5 min",
            'Pasando a la experiencia del usuario, diseñamos dos módulos centrales orientados a la velocidad operativa y a prevenir errores humanos:\n\n• Punto de Venta (POS): Permite buscar productos en tiempo real, filtrar por variantes y seleccionar el medio de pago con recargos o descuentos automáticos. Pero lo más importante es que agregamos un Modal de Confirmación con formato de Ticket Fiscal: antes de guardar la venta, el vendedor visualiza el detalle completo de ítems, cantidades y total. Si detecta un error puede cancelar en el momento, evitando transacciones erróneas y posteriores devoluciones.\n\n• Dashboard Dinámico: Cuenta con métricas clave en vivo (ventas de hoy, stock crítico). Cada métrica es una Tarjeta Expandible: al hacer clic, por ejemplo en "Stock Bajo", la tarjeta se despliega suavemente y muestra la tabla con todos los productos bajo el stock mínimo.\n\nToda la interfaz utiliza modo oscuro con estética glassmorphism, brindando una experiencia moderna y cómoda para largas jornadas de trabajo.'
        ),
        (
            12, "DESARROLLO ASISTIDO POR IA — PROTOCOLO POR FASES", "Lucas Duarte", "~1 min",
            'En cuanto a la metodología, aplicamos un desarrollo asistido por Inteligencia Artificial utilizando Antigravity de Google DeepMind, siguiendo un protocolo estructurado en 5 fases:\n\n1. Fase 1: Modelado conceptual y DER en 3FN.\n2. Fase 2: Esquema DDL, constraints y triggers en PL/pgSQL.\n3. Fase 3: Backend en FastAPI con pool de conexiones y endpoints REST.\n4. Fase 4: Frontend en Jinja2 con modales y componentes expandibles.\n5. Fase 5: Pruebas de concurrencia, sincronización de secuencias y auditoría de integridad.\n\nQueremos destacar que la IA actuó como un co-piloto técnico que aceleró la escritura de código, pero las decisiones de diseño, la lógica relacional y la validación de cada línea fueron dirigidas y controladas 100% por nosotros.'
        ),
        (
            13, "CONCLUSIONES Y CIERRE", "Lucas Duarte", "~1 min",
            'Para cerrar nuestra exposición, queremos compartir los aprendizajes y logros principales:\n\n1. Construimos un sistema Full Stack completamente funcional y adaptado a las necesidades reales de una marroquinería.\n2. La base de datos no es un simple repositorio: es un sistema inteligente y autosuficiente gracias a sus triggers y claves foráneas compuestas.\n3. Confirmamos que la normalización y el álgebra relacional no son meros ejercicios teóricos, sino las bases fundamentales para evitar bugs graves y lograr que una aplicación escale.\n4. Demostramos que el control directo sobre el motor SQL supera la comodidad de las abstracciones ciegas.\n\nLes agradecemos mucho por su tiempo y quedamos a disposición de la cátedra para responder todas sus preguntas.'
        )
    ]

    for num, title, speaker, timing, text in slides_content:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(3)
        run_h = h.add_run(f"DIAPOSITIVA {num}: {title}")
        run_h.font.name = "Arial"
        run_h.font.size = Pt(12.5)
        run_h.font.bold = True
        run_h.font.color.rgb = RGBColor(15, 23, 42)

        p_info = doc.add_paragraph()
        p_info.paragraph_format.space_after = Pt(5)
        run_spk = p_info.add_run(f"🎤 Disertante: {speaker}   |   ⏱️ Tiempo: {timing}")
        run_spk.font.name = "Arial"
        run_spk.font.size = Pt(10)
        run_spk.font.bold = True
        col = RGBColor(2, 132, 199) if "Augusto" in speaker else RGBColor(124, 58, 237)
        run_spk.font.color.rgb = col

        p_text = doc.add_paragraph()
        p_text.paragraph_format.space_after = Pt(8)
        p_text.paragraph_format.line_spacing = 1.15
        run_t = p_text.add_run(text)
        run_t.font.name = "Arial"
        run_t.font.size = Pt(10)
        run_t.font.color.rgb = RGBColor(30, 41, 59)

        # Divisor
        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_after = Pt(6)
        run_d = p_div.add_run("―" * 52)
        run_d.font.color.rgb = RGBColor(203, 213, 225)

    doc_path = "Guion_Presentacion_Augusto_y_Lucas.docx"
    doc.save(doc_path)
    print(f"Docx 50/50 successfully generated at: {doc_path}")

if __name__ == "__main__":
    generate_balanced_docx()
