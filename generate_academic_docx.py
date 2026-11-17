import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_academic_docx():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("DEFENSA DE PROYECTO FINAL: BASES DE DATOS RELACIONALES")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_s = p_sub.add_run("Sistema de Gestión Comercial para Marroquinería — Enfoque en Modelado Relacional, Integridad y Optimización")
    run_s.font.name = "Arial"
    run_s.font.size = Pt(12)
    run_s.font.color.rgb = RGBColor(71, 85, 105)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_m = p_meta.add_run("Disertantes: Augusto Barzola & Lucas Duarte\nDuración estimada: 12 - 14 minutos (División 50/50: ~6.5 min c/u) | Cátedra de Bases de Datos\n")
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
    hdr[2].text = "Ejes Conceptuales de Base de Datos"
    hdr[3].text = "Tiempo"

    for cell in hdr:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    div_data = [
        ("PRIMERA MITAD\nAugusto Barzola", "Slides 1 a 7\n(7 diapositivas)", "• Contexto de Negocio y Dominio de Datos\n• Agenda de Exposición\n• Justificación del Motor Relacional (ACID)\n• Arquitectura de Acceso a Datos y Capas\n• Modelo de Datos — DER (13 tablas relacionales)\n• Teoría de Normalización (1FN, 2FN, 3FN)\n• Triggers en PL/pgSQL y Reglas de Negocio en Motor", "~6.5 min"),
        ("SEGUNDA MITAD\nLucas Duarte", "Slides 8 a 13\n(6 diapositivas)", "• Integridad Referencial: FK Compuesta en Devolución\n• Consultas Complejas y Álgebra Relacional (Push-Down)\n• Fundamentación Técnica: SQL Directo vs ORM (ACID)\n• Interfaz de Gestión como Consumidora de Transacciones\n• Metodología de Diseño y Rol Asistencial de la IA\n• Conclusiones Académicas y Preguntas de Cátedra", "~6.5 min")
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

    # Slides content
    slides_academic = [
        (
            1, "PORTADA — SISTEMA DE GESTIÓN PARA MARROQUINERÍA", "Augusto Barzola", "~30 seg",
            'Buenos días profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy presentamos la defensa de nuestro proyecto final para la cátedra de Bases de Datos.\n\nEl proyecto aborda el diseño formal, la implementación y la optimización de una base de datos relacional orientada a la gestión comercial integral de una marroquinería, desarrollada sobre el motor PostgreSQL con una arquitectura de acceso a datos directa en Python.\n\nEl objetivo central de este desarrollo fue garantizar que la integridad referencial, el aislamiento transaccional y las reglas de negocio críticas residan estrictamente en el motor de base de datos, optimizando además el costo computacional de las consultas analíticas.'
        ),
        (
            2, "ÍNDICE TEMÁTICO — HOJA DE RUTA ACADÉMICA", "Augusto Barzola", "~30 seg",
            'La exposición se encuentra dividida formalmente en dos bloques equitativos de 50%:\n\n• En la primera mitad, abordaré la modelización conceptual y lógica: el problema del dominio de datos, la justificación de un motor ACID, el Diagrama Entidad-Relación de 13 tablas, la demostración formal de la Tercera Forma Normal (3FN) y la implementación de triggers en PL/pgSQL para la automatización atómica del inventario.\n\n• En la segunda mitad, Lucas desarrollará la integridad referencial avanzada mediante claves foráneas compuestas en devoluciones, el modelado y optimización de consultas a través del Álgebra Relacional con push-down de selecciones, la justificación del uso de SQL directo sobre abstracciones ORM, la interacción de la interfaz consumidora y las conclusiones metodológicas.'
        ),
        (
            3, "PROBLEMÁTICA DEL DOMINIO Y SOLUCIÓN RELACIONAL", "Augusto Barzola", "~1 min",
            'El negocio de una marroquinería presenta una complejidad representativa clásica: un mismo producto genérico se descompone en múltiples variantes según dimensiones ortogonales como material, color y tamaño.\n\nLa ausencia de un modelo estructurado genera los problemas clásicos de inconsistencia que estudiamos en la materia:\n1. Anomalías de actualización: redundancia de información descriptiva en múltiples registros.\n2. Inconsistencia de inventario: modificaciones concurrentes sin aislamiento ni actualización atómica.\n3. Falta de integridad referencial: registros de devoluciones sin vínculo verificable con el comprobante de venta original.\n\nNuestra solución consistió en diseñar un esquema relacional normalizado en PostgreSQL donde el motor es la única fuente de verdad, aplicando restricciones declarativas y procedimentales para asegurar la integridad física y lógica de los datos.'
        ),
        (
            4, "ARQUITECTURA DE ACCESO A DATOS Y FLUJO TRANSACCIONAL", "Augusto Barzola", "~1 min",
            'Desde el punto de vista arquitectónico, el sistema prioriza la pureza en el acceso al motor relacional:\n\n1. Motor Relacional (PostgreSQL): Es el núcleo del sistema. Aloja 13 tablas relacionales, constraints CHECK, restricciones de unicidad, claves foráneas compuestas y procedimientos almacenados ejecutados por triggers.\n2. Capa de Servicios de Datos: Desarrollada en Python con FastAPI, actúa como intermediario para exponer los datos y orquestar transacciones explícitas.\n3. Conexión Directa a Datos (psycopg2): Permite la ejecución de sentencias SQL puras y parametrizadas sin capas intermedias que desvirtúen el plan de ejecución.\n4. Interfaz de Acceso a Datos: Actúa exclusivamente como un cliente consumidor que captura las operaciones del usuario y las transforma en transacciones ACID hacia la base de datos.'
        ),
        (
            5, "MODELO DE DATOS — DIAGRAMA ENTIDAD-RELACIÓN (13 TABLAS)", "Augusto Barzola", "~1.5 min",
            'El modelo relacional consta de 13 tablas estructuradas para representar con exactitud el ciclo transaccional:\n\n• Entidades Fuertes o Maestras: "producto", "variante_producto", "venta" y "compra", que constituyen el núcleo de la actividad del negocio.\n• Entidades Débiles y Transaccionales: "detalle_venta", "detalle_compra" y "devolucion", que registran los ítems granulares de cada transacción.\n• Tablas de Dominio o Catálogo: "categoria", "material", "color", "tamano", "proveedor" y "medio_pago", utilizadas para restringir dominios finitos de atributos.\n\nUn aspecto crítico de diseño es el uso de Claves Primarias Compuestas en las entidades débiles, como (id_venta, renglon_venta), lo que formaliza la dependencia de existencia e identificación. Asimismo, todas las asociaciones cuentan con restricciones de clave foránea con cláusulas ON DELETE RESTRICT para evitar registros huérfanos.'
        ),
        (
            6, "NORMALIZACIÓN FORMAL EN TERCERA FORMA NORMAL (3FN)", "Augusto Barzola", "~1.5 min",
            'Un eje central de evaluación es la normalización del esquema, el cual satisface estrictamente la Tercera Forma Normal (3FN):\n\n• Primera Forma Normal (1FN): Todos los dominios de atributos son atómicos. No existen listas, arreglos ni grupos repetitivos dentro de una misma columna.\n• Segunda Forma Normal (2FN): Se encuentra en 1FN y cada atributo no primario posee dependencia funcional completa respecto a la clave primaria. En entidades compuestas como "detalle_venta", atributos como cantidad y precio unitario dependen de la totalidad de la clave (id_venta, renglon_venta) y no de una parte de ella.\n• Tercera Forma Normal (3FN): Se encuentra en 2FN y ningún atributo no-clave depende transitivamente de la clave primaria (X → Y → Z).\n\nDemostración práctica: Si en "variante_producto" hubiésemos almacenado la descripción del color o material, tendríamos dependencias transitivas: id_variante determina id_color, y este determina nombre_color. Al aislar "color" en una relación independiente, eliminamos anomalías de inserción, actualización y borrado.'
        ),
        (
            7, "TRIGGERS EN PL/PGSQL: AUTOMATIZACIÓN EN EL MOTOR", "Augusto Barzola", "~1.5 min",
            'Para garantizar que las reglas de negocio de inventario se cumplan sin depender de la aplicación, implementamos Triggers en PL/pgSQL directamente en el motor:\n\n• Al producirse un evento INSERT sobre "detalle_venta", se dispara el trigger "trg_stock_venta", ejecutando una función que resta atómicamente el stock en "variante_producto" utilizando el pseudorregistro "NEW.cantidad".\n• De forma recíproca, al insertarse registros en "detalle_compra", el trigger correspondiente incrementa el stock disponible.\n\nLa relevancia académica de esta solución radica en que la regla de integridad de stock queda blindada en el motor. Si un operador ingresa información mediante consola SQL, procesos por lotes o scripts externos, el trigger se dispara indefectiblemente, garantizando consistencia transaccional absoluta.\n\n[TRANSICIÓN]: Habiendo expuesto el modelo relacional, la normalización y la lógica procedural en el motor, le cedo la palabra a Lucas para abordar la integridad en devoluciones, el análisis de álgebra relacional y las consultas complejas.'
        ),
        (
            8, "TABLA DEVOLUCIÓN: INTEGRIDAD CON CLAVE FORÁNEA COMPUESTA", "Lucas Duarte", "~1.5 min",
            'Gracias Augusto. Continuando con los aspectos críticos de integridad referencial, analizamos el diseño formal de la entidad "devolucion".\n\nEl problema teórico y práctico consistía en: ¿Cómo garantizar que no se pueda registrar una devolución de un producto que jamás formó parte de esa venta específica?\n\nSi hubiésemos definido una clave foránea simple referenciando únicamente a "id_venta", el motor solo verificaría la existencia del comprobante cabecera, permitiendo registrar devoluciones inconsistentes o artículos ajenos al ticket.\n\nLa solución implementada fue definir una Clave Foránea Compuesta sobre (id_venta, renglon_venta) que referencia exactamente a la clave primaria de "detalle_venta". De esta manera, el motor valida de forma determinística la existencia física de la línea vendida. Si el par no existe en el detalle, PostgreSQL aborta la operación y rechaza el registro por violación de Foreign Key, garantizando integridad referencial estricta.'
        ),
        (
            9, "ÁLGEBRA RELACIONAL Y HEURÍSTICA DE PUSH-DOWN", "Lucas Duarte", "~2 min",
            'Implementamos 6 consultas complejas con agrupaciones y uniones múltiples. Para evaluar formalmente la consulta de recaudación diaria por producto, modelamos su Árbol de Álgebra Relacional y analizamos su optimización:\n\n• En el Árbol Canónico o No Optimizado, se computan sucesivamente las reuniones naturales (JOINs) de todas las tuplas históricas de "venta", "detalle_venta", "variante" y "producto", y recién en el nodo superior se aplica la selección sigma (fecha = fecha_actual). Esta aproximación es computacionalmente ineficiente debido a la gran cardinalidad de los conjuntos intermedios generados.\n\n• En el Árbol Optimizado, aplicamos la heurística formal de Push-Down de Selecciones: conmutar el operador de selección sigma descendiéndolo a través del árbol hasta alcanzar la relación base "venta". Al filtrar las ventas del día previo a la operación de Join, la cardinalidad de tuplas intermedias se reduce en varios órdenes de magnitud, optimizando el uso de memoria de trabajo (work_mem) y reduciendo el tiempo de procesamiento en el motor.'
        ),
        (
            10, "FUNDAMENTACIÓN TÉCNICA: SQL DIRECTO VS ABSTRACCIONES ORM", "Lucas Duarte", "~1 min",
            'Una decisión clave de arquitectura fue prescindir de un ORM y ejecutar sentencias SQL puras mediante psycopg2. Fundamentamos esta elección en principios propios de la disciplina:\n\n1. Control absoluto de transacciones ACID: Administramos de forma explícita los límites transaccionales mediante bloques BEGIN, COMMIT y ROLLBACK ante excepciones, asegurando atomicidad y durabilidad completas.\n2. Transparencia en el plan de ejecución: Los ORM generan sentencias autogeneradas que a menudo ocultan planes subóptimos o lecturas anidadas indeseadas. Con SQL directo garantizamos visibilidad total del plan que procesa el optimizador.\n3. Uso de SQL parametrizado directo: Empleamos paso de argumentos por parámetros para optimizar la reutilización del plan de ejecución en el motor y eliminar cualquier riesgo de inyección SQL.'
        ),
        (
            11, "INTERFAZ DE ACCESO A DATOS Y GESTIÓN DE TRANSACCIONES", "Lucas Duarte", "~1.5 min",
            'Como valor agregado para la gestión operativa, desarrollamos una Interfaz de Acceso a Datos que funciona estrictamente como cliente de las transacciones del motor:\n\n• En el Punto de Venta: Diseñamos un flujo de verificación previa. Antes de emitir el comando transaccional hacia PostgreSQL, el usuario visualiza una confirmación que consolida los ítems calculados. Esto previene el envío de transacciones erróneas que exigirían posteriores transacciones compensatorias de anulación o devolución en la base de datos.\n\n• En el Módulo de Monitoreo: La interfaz consume consultas agregadas optimizadas que leen en tiempo real métricas de inventario crítico y ventas diarias, demostrando cómo una visualización clara depende directamente de una base de datos normalizada y consultas indexadas eficientes.'
        ),
        (
            12, "METODOLOGÍA DE DISEÑO Y ROL ASISTENCIAL DE LA IA", "Lucas Duarte", "~1 min",
            'Respecto a la metodología de desarrollo, aplicamos un protocolo estructurado por fases donde la Inteligencia Artificial cumplió un rol secundario y acotado:\n\nQueremos enfatizar que el diseño conceptual, la elaboración del Diagrama Entidad-Relación, la aplicación formal de la Tercera Forma Normal, la definición de claves compuestas y la formulación de expresiones de Álgebra Relacional fueron concebidos, calculados y validados íntegramente por nosotros como autores del proyecto.\n\nLa herramienta de IA actuó únicamente como un asistente mecánico de apoyo para agilizar el tipeo del código DDL extenso y el boilerplate de conexión, manteniendo el equipo el control técnico y decisional en cada etapa del desarrollo.'
        ),
        (
            13, "CONCLUSIONES ACADÉMICAS Y CIERRE", "Lucas Duarte", "~1 min",
            'Para concluir la defensa del proyecto, destacamos las siguientes conclusiones técnicas:\n\n1. Demostramos que la robustez y consistencia de un sistema no debe depender del software de aplicación, sino de las garantías formales que provee el motor relacional mediante esquemas normalizados, triggers y constraints de clave foránea compuesta.\n2. La normalización en 3FN y las técnicas de optimización en Álgebra Relacional como el push-down de selecciones no son conceptos teóricos abstractos, sino fundamentos de ingeniería indispensables para el rendimiento y la escalabilidad de bases de datos relacionales.\n3. El control explícito sobre las transacciones y consultas garantiza previsibilidad y rigor en el comportamiento del sistema.\n\nAgradecemos a la cátedra por su atención y quedamos a su entera disposición para responder las preguntas sobre el proyecto.'
        )
    ]

    for num, title, speaker, timing, text in slides_academic:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(3)
        run_h = h.add_run(f"DIAPOSITIVA {num}: {title}")
        run_h.font.name = "Arial"
        run_h.font.size = Pt(12)
        run_h.font.bold = True
        run_h.font.color.rgb = RGBColor(15, 23, 42)

        p_info = doc.add_paragraph()
        p_info.paragraph_format.space_after = Pt(5)
        run_spk = p_info.add_run(f"Disertante: {speaker}   |   Tiempo sugerido: {timing}")
        run_spk.font.name = "Arial"
        run_spk.font.size = Pt(9.5)
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
    print(f"Academic Guion DOCX saved successfully: {doc_path}")

if __name__ == "__main__":
    generate_academic_docx()
