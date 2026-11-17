import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_academic_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Paleta sobria y formal para cátedra académica
    BG_COLOR = RGBColor(15, 23, 42)        # Azul pizarra oscuro
    CARD_BG = RGBColor(30, 41, 59)         # Contenedor sobrio
    CARD_BORDER = RGBColor(51, 65, 85)     # Borde sutil
    ACCENT_CYAN = RGBColor(56, 189, 248)   # Augusto
    ACCENT_INDIGO = RGBColor(129, 140, 248)# Lucas
    TEXT_WHITE = RGBColor(248, 250, 252)   # Texto principal
    TEXT_MUTED = RGBColor(148, 163, 184)   # Texto secundario
    CODE_BG = RGBColor(2, 6, 23)           # Fondo consola SQL

    def add_base_slide(title_text, speaker_name, is_int2=False):
        slide = prs.slides.add_slide(blank_layout)
        
        # Fondo general
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

        # Badge del expositor
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.48), Inches(3.6), Inches(0.42))
        badge.fill.solid()
        badge.fill.fore_color.rgb = CARD_BG
        badge.line.color.rgb = ACCENT_INDIGO if is_int2 else ACCENT_CYAN
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = f"Disertante: {speaker_name}"
        p_b.font.size = Pt(12)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_INDIGO if is_int2 else ACCENT_CYAN
        p_b.alignment = PP_ALIGN.CENTER

        # Título académico
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(25)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        return slide

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================
    # SLIDE 1: PORTADA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_COLOR
    bg1.line.fill.background()

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.933), Inches(5.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = CARD_BORDER

    tf1 = card1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "SISTEMA DE GESTIÓN PARA MARROQUINERÍA"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN
    p1.alignment = PP_ALIGN.CENTER

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Diseño Formal, Integridad y Optimización de una Base de Datos Relacional"
    p1_sub.font.size = Pt(17)
    p1_sub.font.color.rgb = TEXT_MUTED
    p1_sub.alignment = PP_ALIGN.CENTER

    p1_space = tf1.add_paragraph()
    p1_space.text = "\nDefensa de Proyecto Final — Cátedra de Bases de Datos\n"
    p1_space.font.size = Pt(15)
    p1_space.font.color.rgb = ACCENT_INDIGO
    p1_space.alignment = PP_ALIGN.CENTER

    p1_authors = tf1.add_paragraph()
    p1_authors.text = "Autores (División Equitativa 50/50):\nAugusto Barzola (Slides 1 a 7)   •   Lucas Duarte (Slides 8 a 13)"
    p1_authors.font.size = Pt(17)
    p1_authors.font.bold = True
    p1_authors.font.color.rgb = TEXT_WHITE
    p1_authors.alignment = PP_ALIGN.CENTER

    set_notes(s1, 'GUION HABLADO (Augusto Barzola):\n"Buenos días profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy presentamos la defensa de nuestro proyecto final para la cátedra de Bases de Datos.\n\nEl proyecto aborda el diseño formal, la implementación y la optimización de una base de datos relacional orientada a la gestión comercial integral de una marroquinería, desarrollada sobre el motor PostgreSQL con una arquitectura de acceso a datos directa en Python.\n\nEl objetivo central de este desarrollo fue garantizar que la integridad referencial, el aislamiento transaccional y las reglas de negocio críticas residan estrictamente en el motor de base de datos, optimizando además el costo computacional de las consultas analíticas."')

    # ==========================================
    # SLIDE 2: AGENDA ACADÉMICA
    # ==========================================
    s2 = add_base_slide("Estructura de la Exposición Académica", "Augusto Barzola")
    c2_1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c2_1.fill.solid()
    c2_1.fill.fore_color.rgb = CARD_BG
    c2_1.line.color.rgb = ACCENT_CYAN
    tf2_1 = c2_1.text_frame
    tf2_1.word_wrap = True
    tf2_1.text = "Bloque I — Modelado e Integridad (Augusto Barzola)"
    tf2_1.paragraphs[0].font.size = Pt(15)
    tf2_1.paragraphs[0].font.bold = True
    tf2_1.paragraphs[0].font.color.rgb = ACCENT_CYAN

    items_b1 = [
        "1. Problemática del Dominio y Solución Relacional",
        "2. Arquitectura de Acceso a Datos y Flujo Transaccional",
        "3. Modelo Conceptual y DER (13 tablas relacionales)",
        "4. Teoría de Normalización: Demostración en 3FN",
        "5. Lógica Procedural en Motor: Triggers en PL/pgSQL",
        "6. Control Atómico de Inventario bajo Transacciones ACID"
    ]
    for it in items_b1:
        p = tf2_1.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c2_2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c2_2.fill.solid()
    c2_2.fill.fore_color.rgb = CARD_BG
    c2_2.line.color.rgb = ACCENT_INDIGO
    tf2_2 = c2_2.text_frame
    tf2_2.word_wrap = True
    tf2_2.text = "Bloque II — Optimización y Consultas (Lucas Duarte)"
    tf2_2.paragraphs[0].font.size = Pt(15)
    tf2_2.paragraphs[0].font.bold = True
    tf2_2.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    items_b2 = [
        "7. Integridad Referencial Avanzada: FK Compuesta en Devolución",
        "8. Consultas Complejas y Álgebra Relacional (Push-Down)",
        "9. Fundamentación Técnica: SQL Directo vs Abstracciones ORM",
        "10. Interfaz de Acceso a Datos como Cliente Transaccional",
        "11. Metodología de Diseño y Rol Asistencial de la IA",
        "12. Conclusiones y Defensa ante Preguntas de Cátedra"
    ]
    for it in items_b2:
        p = tf2_2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s2, 'GUION HABLADO (Augusto Barzola):\n"La exposición se encuentra dividida formalmente en dos bloques equitativos de 50%:\n\n• En la primera mitad, abordaré la modelización conceptual y lógica: el problema del dominio de datos, la justificación de un motor ACID, el Diagrama Entidad-Relación de 13 tablas, la demostración formal de la Tercera Forma Normal (3FN) y la implementación de triggers en PL/pgSQL para la automatización atómica del inventario.\n\n• En la segunda mitad, Lucas desarrollará la integridad referencial avanzada mediante claves foráneas compuestas en devoluciones, el modelado y optimización de consultas a través del Álgebra Relacional con push-down de selecciones, la justificación del uso de SQL directo sobre abstracciones ORM, la interacción de la interfaz consumidora y las conclusiones metodológicas."')

    # ==========================================
    # SLIDE 3: PROBLEMA Y SOLUCIÓN RELACIONAL
    # ==========================================
    s3 = add_base_slide("Problemática del Dominio y Solución Relacional", "Augusto Barzola")
    c3_1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c3_1.fill.solid()
    c3_1.fill.fore_color.rgb = CARD_BG
    c3_1.line.color.rgb = RGBColor(239, 68, 68)
    tf3_1 = c3_1.text_frame
    tf3_1.word_wrap = True
    tf3_1.text = "Riesgos de Inconsistencia en Datos"
    tf3_1.paragraphs[0].font.size = Pt(16)
    tf3_1.paragraphs[0].font.bold = True
    tf3_1.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    prob_items = [
        "Complejidad multidimensional: un producto posee variantes ortogonales de material, color y tamaño.",
        "Anomalías de redundancia y actualización por registros desnormalizados.",
        "Modificaciones concurrentes sin aislamiento ni control transaccional.",
        "Devoluciones inconsistentes sin vínculo referencial con la venta original.",
        "Imposibilidad de auditar el saldo real de inventario en tiempo real."
    ]
    for it in prob_items:
        p = tf3_1.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c3_2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c3_2.fill.solid()
    c3_2.fill.fore_color.rgb = CARD_BG
    c3_2.line.color.rgb = RGBColor(34, 197, 94)
    tf3_2 = c3_2.text_frame
    tf3_2.word_wrap = True
    tf3_2.text = "Garantías del Modelo Relacional"
    tf3_2.paragraphs[0].font.size = Pt(16)
    tf3_2.paragraphs[0].font.bold = True
    tf3_2.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    sol_items = [
        "Esquema relacional en PostgreSQL normalizado formalmente en 3FN.",
        "Propiedades ACID garantizadas a nivel de motor en todas las operaciones.",
        "Reglas de inventario gobernadas por Triggers procedurales en PL/pgSQL.",
        "Integridad referencial blindada mediante claves foráneas compuestas.",
        "Consultas complejas optimizadas para reportería y balance transaccional."
    ]
    for it in sol_items:
        p = tf3_2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s3, 'GUION HABLADO (Augusto Barzola):\n"El negocio de una marroquinería presenta una complejidad representativa clásica: un mismo producto genérico se descompone en múltiples variantes según dimensiones ortogonales como material, color y tamaño.\n\nLa ausencia de un modelo estructurado genera los problemas clásicos de inconsistencia que estudiamos en la materia:\n1. Anomalías de actualización: redundancia de información descriptiva en múltiples registros.\n2. Inconsistencia de inventario: modificaciones concurrentes sin aislamiento ni actualización atómica.\n3. Falta de integridad referencial: registros de devoluciones sin vínculo verificable con el comprobante de venta original.\n\nNuestra solución consistió en diseñar un esquema relacional normalizado en PostgreSQL donde el motor es la única fuente de verdad, aplicando restricciones declarativas y procedimentales para asegurar la integridad física y lógica de los datos."')

    # ==========================================
    # SLIDE 4: ARQUITECTURA DE ACCESO A DATOS
    # ==========================================
    s4 = add_base_slide("Arquitectura de Acceso a Datos y Capas Transaccionales", "Augusto Barzola")
    c4_left = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(6.5), Inches(4.8))
    c4_left.fill.solid()
    c4_left.fill.fore_color.rgb = CARD_BG
    c4_left.line.color.rgb = CARD_BORDER
    tf4_l = c4_left.text_frame
    tf4_l.word_wrap = True
    tf4_l.text = "Componentes de la Arquitectura"
    tf4_l.paragraphs[0].font.size = Pt(16)
    tf4_l.paragraphs[0].font.bold = True
    tf4_l.paragraphs[0].font.color.rgb = ACCENT_CYAN

    arch_bullets = [
        "Motor Relacional (PostgreSQL): Núcleo de persistencia, 13 tablas, restricciones CHECK, foreign keys y triggers en PL/pgSQL.",
        "Capa de Servicios de Datos (FastAPI): API REST encargada del mapeo de datos y orquestación de transacciones hacia el motor.",
        "Acceso Directo a Datos (psycopg2): Ejecución directa de SQL puro y parametrizado sin capas de abstracción ORM.",
        "Interfaz de Acceso a Datos: Cliente visual que captura operaciones y emite transacciones hacia el motor para asegurar consistencia."
    ]
    for it in arch_bullets:
        p = tf4_l.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c4_right = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(1.9), Inches(4.8), Inches(4.8))
    c4_right.fill.solid()
    c4_right.fill.fore_color.rgb = CODE_BG
    c4_right.line.color.rgb = ACCENT_CYAN
    tf4_r = c4_right.text_frame
    tf4_r.word_wrap = True
    tf4_r.text = "Flujo Transaccional\n\n"
    tf4_r.paragraphs[0].font.size = Pt(15)
    tf4_r.paragraphs[0].font.bold = True
    tf4_r.paragraphs[0].font.color.rgb = ACCENT_CYAN

    diagram_text = (
        "[ Interfaz de Acceso a Datos ]\n"
        "Captura y confirmación de operaciones\n"
        "       ↕  (Llamadas de servicio)\n\n"
        "[ Capa de Servicios Backend ]\n"
        "Orquestación transaccional (Python)\n"
        "       ↕  (SQL Parametrizado Directo)\n\n"
        "[ Motor Relacional PostgreSQL ]\n"
        "13 Tablas • Triggers • Constraints • ACID"
    )
    p_diag = tf4_r.add_paragraph()
    p_diag.text = diagram_text
    p_diag.font.size = Pt(12)
    p_diag.font.color.rgb = TEXT_WHITE

    set_notes(s4, 'GUION HABLADO (Augusto Barzola):\n"Desde el punto de vista arquitectónico, el sistema prioriza la pureza en el acceso al motor relacional:\n\n1. Motor Relacional (PostgreSQL): Es el núcleo del sistema. Aloja 13 tablas relacionales, constraints CHECK, restricciones de unicidad, claves foráneas compuestas y procedimientos almacenados ejecutados por triggers.\n2. Capa de Servicios de Datos: Desarrollada en Python con FastAPI, actúa como intermediario para exponer los datos y orquestar transacciones explícitas.\n3. Conexión Directa a Datos (psycopg2): Permite la ejecución de sentencias SQL puras y parametrizadas sin capas intermedias que desvirtúen el plan de ejecución.\n4. Interfaz de Acceso a Datos: Actúa exclusivamente como un cliente consumidor que captura las operaciones del usuario y las transforma en transacciones ACID hacia la base de datos."')

    # ==========================================
    # SLIDE 5: DER (13 TABLAS)
    # ==========================================
    s5 = add_base_slide("Modelo de Datos — Diagrama Entidad-Relación (13 Tablas)", "Augusto Barzola")
    der_cats = [
        ("Entidades Fuertes / Maestras", "producto\nvariante_producto\nventa\ncompra", Inches(0.8), ACCENT_CYAN),
        ("Entidades Débiles / Transaccionales", "detalle_venta\ndetalle_compra\ndevolucion", Inches(4.8), ACCENT_INDIGO),
        ("Tablas de Dominio / Catálogo", "categoria\nmaterial\ncolor\ntamano\nproveedor\nmedio_pago", Inches(8.8), RGBColor(34, 197, 94))
    ]
    for title, tbls, left_pos, col in der_cats:
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(3.7), Inches(3.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        tf = c.text_frame
        tf.word_wrap = True
        tf.text = title
        tf.paragraphs[0].font.size = Pt(15)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = col

        for t in tbls.split("\n"):
            p = tf.add_paragraph()
            p.text = "• " + t
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_WHITE

    c5_b = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.5))
    c5_b.fill.solid()
    c5_b.fill.fore_color.rgb = CARD_BG
    c5_b.line.color.rgb = CARD_BORDER
    tf5_b = c5_b.text_frame
    tf5_b.word_wrap = True
    tf5_b.text = "Rigor Relacional Aplicado:"
    tf5_b.paragraphs[0].font.size = Pt(14)
    tf5_b.paragraphs[0].font.bold = True
    tf5_b.paragraphs[0].font.color.rgb = ACCENT_CYAN
    p_b1 = tf5_b.add_paragraph()
    p_b1.text = "• Claves primarias compuestas en entidades débiles: (id_venta, renglon_venta) y (id_compra, renglon_compra)."
    p_b1.font.size = Pt(12)
    p_b1.font.color.rgb = TEXT_MUTED
    p_b2 = tf5_b.add_paragraph()
    p_b2.text = "• Restricciones de integridad referencial: Cláusulas ON DELETE RESTRICT en todas las claves foráneas para evitar registros huérfanos."
    p_b2.font.size = Pt(12)
    p_b2.font.color.rgb = TEXT_MUTED

    set_notes(s5, 'GUION HABLADO (Augusto Barzola):\n"El modelo relacional consta de 13 tablas estructuradas para representar con exactitud el ciclo transaccional:\n\n• Entidades Fuertes o Maestras: producto, variante_producto, venta y compra, que constituyen el núcleo de la actividad del negocio.\n• Entidades Débiles y Transaccionales: detalle_venta, detalle_compra y devolucion, que registran los ítems granulares de cada transacción.\n• Tablas de Dominio o Catálogo: categoria, material, color, tamano, proveedor y medio_pago, utilizadas para restringir dominios finitos de atributos.\n\nUn aspecto crítico de diseño es el uso de Claves Primarias Compuestas en las entidades débiles, como (id_venta, renglon_venta), lo que formaliza la dependencia de existencia e identificación. Asimismo, todas las asociaciones cuentan con restricciones de clave foránea con cláusulas ON DELETE RESTRICT para evitar registros huérfanos."')

    # ==========================================
    # SLIDE 6: 3FN
    # ==========================================
    s6 = add_base_slide("Normalización Formal en Tercera Forma Normal (3FN)", "Augusto Barzola")
    c6_top = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.7), Inches(2.3))
    c6_top.fill.solid()
    c6_top.fill.fore_color.rgb = CARD_BG
    c6_top.line.color.rgb = CARD_BORDER
    tf6_t = c6_top.text_frame
    tf6_t.word_wrap = True
    tf6_t.text = "Demostración de las Formas Normales"
    tf6_t.paragraphs[0].font.size = Pt(16)
    tf6_t.paragraphs[0].font.bold = True
    tf6_t.paragraphs[0].font.color.rgb = ACCENT_CYAN

    fn_rules = [
        "1FN (Atributos Atómicos): Cada columna almacena valores indivisibles; no existen arreglos ni grupos repetitivos.",
        "2FN (Dependencia Completa): En relaciones con clave compuesta (ej: detalle_venta), los atributos no-clave (precio, cantidad) dependen funcionalmente de la totalidad de la clave (id_venta, renglon_venta).",
        "3FN (Ausencia de Dependencia Transitiva): Ningún atributo no-clave depende funcionalmente de otro atributo no-clave (X → Y → Z)."
    ]
    for r in fn_rules:
        p = tf6_t.add_paragraph()
        p.text = "• " + r
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c6_bad = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.4))
    c6_bad.fill.solid()
    c6_bad.fill.fore_color.rgb = CARD_BG
    c6_bad.line.color.rgb = RGBColor(239, 68, 68)
    tf6_bad = c6_bad.text_frame
    tf6_bad.word_wrap = True
    tf6_bad.text = "❌ Esquema No Normalizado (Anomalías)"
    tf6_bad.paragraphs[0].font.size = Pt(14)
    tf6_bad.paragraphs[0].font.bold = True
    tf6_bad.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)
    p_b_text = tf6_bad.add_paragraph()
    p_b_text.text = "variante_producto(id_variante, color='Negro', material='Cuero')\n\nDependencia Transitiva: id_variante → color.\nAnomalía: Modificar la denominación exige UPDATE masivo con riesgo de inconsistencia."
    p_b_text.font.size = Pt(12)
    p_b_text.font.color.rgb = TEXT_MUTED

    c6_good = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.4))
    c6_good.fill.solid()
    c6_good.fill.fore_color.rgb = CARD_BG
    c6_good.line.color.rgb = RGBColor(34, 197, 94)
    tf6_good = c6_good.text_frame
    tf6_good.word_wrap = True
    tf6_good.text = "✅ Esquema en 3FN (Diseño Aplicado)"
    tf6_good.paragraphs[0].font.size = Pt(14)
    tf6_good.paragraphs[0].font.bold = True
    tf6_good.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)
    p_g_text = tf6_good.add_paragraph()
    p_g_text.text = "variante_producto(id_variante, id_color, id_material)\ncolor(id_color, nombre_color)\n\nBeneficio: Redundancia mínima, consistencia garantizada y actualización atómica en una única tupla."
    p_g_text.font.size = Pt(12)
    p_g_text.font.color.rgb = TEXT_MUTED

    set_notes(s6, 'GUION HABLADO (Augusto Barzola):\n"Un eje central de evaluación es la normalización del esquema, el cual satisface estrictamente la Tercera Forma Normal (3FN):\n\n• Primera Forma Normal (1FN): Todos los dominios de atributos son atómicos. No existen listas, arreglos ni grupos repetitivos dentro de una misma columna.\n• Segunda Forma Normal (2FN): Se encuentra en 1FN y cada atributo no primario posee dependencia funcional completa respecto a la clave primaria. En entidades compuestas como "detalle_venta", atributos como cantidad y precio unitario dependen de la totalidad de la clave (id_venta, renglon_venta) y no de una parte de ella.\n• Tercera Forma Normal (3FN): Se encuentra en 2FN y ningún atributo no-clave depende transitivamente de la clave primaria (X → Y → Z).\n\nDemostración práctica: Si en "variante_producto" hubiésemos almacenado la descripción del color o material, tendríamos dependencias transitivas: id_variante determina id_color, y este determina nombre_color. Al aislar "color" en una relación independiente, eliminamos anomalías de inserción, actualización y borrado."')

    # ==========================================
    # SLIDE 7: TRIGGERS EN PL/PGSQL
    # ==========================================
    s7 = add_base_slide("Lógica Procedural en Motor: Triggers en PL/pgSQL", "Augusto Barzola")
    c7_left = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.8))
    c7_left.fill.solid()
    c7_left.fill.fore_color.rgb = CARD_BG
    c7_left.line.color.rgb = ACCENT_CYAN
    tf7_l = c7_left.text_frame
    tf7_l.word_wrap = True
    tf7_l.text = "Reglas de Negocio a Nivel Motor"
    tf7_l.paragraphs[0].font.size = Pt(16)
    tf7_l.paragraphs[0].font.bold = True
    tf7_l.paragraphs[0].font.color.rgb = ACCENT_CYAN

    trg_points = [
        "El inventario se recalcula de forma ATÓMICA en el motor PostgreSQL.",
        "detalle_venta (INSERT) → Trigger decrementa stock_actual en variante_producto.",
        "detalle_compra (INSERT) → Trigger incrementa stock_actual al ingresar mercadería.",
        "Independencia absoluta: el trigger se dispara ante cualquier canal de inserción (consola SQL, procesos batch o scripts externos).",
        "El pseudorregistro NEW captura los atributos de la tupla entrante."
    ]
    for p in trg_points:
        p_node = tf7_l.add_paragraph()
        p_node.text = "• " + p
        p_node.font.size = Pt(13)
        p_node.font.color.rgb = TEXT_WHITE

    c7_right = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.8))
    c7_right.fill.solid()
    c7_right.fill.fore_color.rgb = CODE_BG
    c7_right.line.color.rgb = CARD_BORDER
    tf7_r = c7_right.text_frame
    tf7_r.word_wrap = True
    tf7_r.text = "Definición Procedural en PL/pgSQL:\n"
    tf7_r.paragraphs[0].font.size = Pt(13)
    tf7_r.paragraphs[0].font.bold = True
    tf7_r.paragraphs[0].font.color.rgb = ACCENT_CYAN

    trg_code = (
        "CREATE OR REPLACE FUNCTION actualizar_stock_venta()\n"
        "RETURNS TRIGGER AS $$\n"
        "BEGIN\n"
        "    UPDATE variante_producto\n"
        "    SET stock_actual = stock_actual - NEW.cantidad\n"
        "    WHERE id_variante = NEW.id_variante;\n"
        "    RETURN NEW;\n"
        "END;\n"
        "$$ LANGUAGE plpgsql;\n\n"
        "CREATE TRIGGER trigger_stock_venta\n"
        "AFTER INSERT ON detalle_venta\n"
        "FOR EACH ROW\n"
        "EXECUTE FUNCTION actualizar_stock_venta();"
    )
    p_code = tf7_r.add_paragraph()
    p_code.text = trg_code
    p_code.font.size = Pt(11)
    p_code.font.color.rgb = ACCENT_CYAN

    set_notes(s7, 'GUION HABLADO (Augusto Barzola):\n"Para garantizar que las reglas de negocio de inventario se cumplan sin depender de la aplicación, implementamos Triggers en PL/pgSQL directamente en el motor:\n\n• Al producirse un evento INSERT sobre "detalle_venta", se dispara el trigger "trg_stock_venta", ejecutando una función que resta atómicamente el stock en "variante_producto" utilizando el pseudorregistro "NEW.cantidad".\n• De forma recíproca, al insertarse registros en "detalle_compra", el trigger correspondiente incrementa el stock disponible.\n\nLa relevancia académica de esta solución radica en que la regla de integridad de stock queda blindada en el motor. Si un operador ingresa información mediante consola SQL, procesos por lotes o scripts externos, el trigger se dispara indefectiblemente, garantizando consistencia transaccional absoluta.\n\n[TRANSICIÓN]: Habiendo expuesto el modelo relacional, la normalización y la lógica procedural en el motor, le cedo la palabra a Lucas para abordar la integridad en devoluciones, el análisis de álgebra relacional y las consultas complejas."')

    # ==========================================
    # SLIDE 8: TABLA DEVOLUCIÓN (FK COMPUESTA)
    # ==========================================
    s8 = add_base_slide("Integridad Referencial: Clave Foránea Compuesta en Devolución", "Lucas Duarte", is_int2=True)
    c8_t = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.7), Inches(1.2))
    c8_t.fill.solid()
    c8_t.fill.fore_color.rgb = CARD_BG
    c8_t.line.color.rgb = RGBColor(234, 179, 8)
    tf8_t = c8_t.text_frame
    tf8_t.word_wrap = True
    tf8_t.text = "🎯 Problema de Integridad Referencial a Resolver:"
    tf8_t.paragraphs[0].font.size = Pt(14)
    tf8_t.paragraphs[0].font.bold = True
    tf8_t.paragraphs[0].font.color.rgb = RGBColor(234, 179, 8)
    p_prob = tf8_t.add_paragraph()
    p_prob.text = "¿Cómo impedir en el motor la devolución de un ítem que nunca formó parte de la venta referenciada?"
    p_prob.font.size = Pt(13)
    p_prob.font.color.rgb = TEXT_WHITE

    c8_code = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(6.0), Inches(3.4))
    c8_code.fill.solid()
    c8_code.fill.fore_color.rgb = CODE_BG
    c8_code.line.color.rgb = CARD_BORDER
    tf8_c = c8_code.text_frame
    tf8_c.word_wrap = True
    tf8_c.text = "DDL Riguroso de la Tabla devolucion:\n"
    tf8_c.paragraphs[0].font.size = Pt(13)
    tf8_c.paragraphs[0].font.bold = True
    tf8_c.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    dev_ddl = (
        "CREATE TABLE devolucion (\n"
        "    id_devolucion SERIAL PRIMARY KEY,\n"
        "    id_venta INTEGER NOT NULL,\n"
        "    renglon_venta INTEGER NOT NULL,\n"
        "    cantidad_devuelta INT CHECK (cantidad_devuelta > 0),\n"
        "    motivo TEXT,\n"
        "    fecha_devolucion DATE DEFAULT CURRENT_DATE,\n\n"
        "    -- FK COMPUESTA:\n"
        "    CONSTRAINT fk_devolucion_detalle\n"
        "        FOREIGN KEY (id_venta, renglon_venta)\n"
        "        REFERENCES detalle_venta(id_venta, renglon_venta)\n"
        "        ON DELETE RESTRICT\n"
        ");"
    )
    p_dev_c = tf8_c.add_paragraph()
    p_dev_c.text = dev_ddl
    p_dev_c.font.size = Pt(10.5)
    p_dev_c.font.color.rgb = ACCENT_INDIGO

    c8_why = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(3.3), Inches(5.4), Inches(3.4))
    c8_why.fill.solid()
    c8_why.fill.fore_color.rgb = CARD_BG
    c8_why.line.color.rgb = ACCENT_INDIGO
    tf8_w = c8_why.text_frame
    tf8_w.word_wrap = True
    tf8_w.text = "Garantía Formal en el Motor"
    tf8_w.paragraphs[0].font.size = Pt(15)
    tf8_w.paragraphs[0].font.bold = True
    tf8_w.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    dev_points = [
        "Insuficiencia de FK simple: Una FK referenciando solo a id_venta valida la existencia de la venta, pero permitiría registrar devoluciones de productos inexistentes en dicho comprobante.",
        "FK compuesta determinística: La restricción obliga a la coincidencia simultánea de (id_venta, renglon_venta) en detalle_venta.",
        "Rechazo nativo: Si la tupla no existe, el motor aborta la transacción y emite una excepción de clave foránea.",
        "Integridad referencial estricta garantizada por el SGBD."
    ]
    for p in dev_points:
        p_w = tf8_w.add_paragraph()
        p_w.text = "• " + p
        p_w.font.size = Pt(11.5)
        p_w.font.color.rgb = TEXT_WHITE

    set_notes(s8, 'GUION HABLADO (Lucas Duarte):\n"Gracias Augusto. Continuando con los aspectos críticos de integridad referencial, analizamos el diseño formal de la entidad "devolucion".\n\nEl problema teórico y práctico consistía en: ¿Cómo garantizar que no se pueda registrar una devolución de un producto que jamás formó parte de esa venta específica?\n\nSi hubiésemos definido una clave foránea simple referenciando únicamente a "id_venta", el motor solo verificaría la existencia del comprobante cabecera, permitiendo registrar devoluciones inconsistentes o artículos ajenos al ticket.\n\nLa solución implementada fue definir una Clave Foránea Compuesta sobre (id_venta, renglon_venta) que referencia exactamente a la clave primaria de "detalle_venta". De esta manera, el motor valida de forma determinística la existencia física de la línea vendida. Si el par no existe en el detalle, PostgreSQL aborta la operación y rechaza el registro por violación de Foreign Key, garantizando integridad referencial estricta."')

    # ==========================================
    # SLIDE 9: ÁLGEBRA RELACIONAL & PUSH-DOWN
    # ==========================================
    s9 = add_base_slide("Consultas Complejas y Álgebra Relacional (Push-Down)", "Lucas Duarte", is_int2=True)
    c9_l = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c9_l.fill.solid()
    c9_l.fill.fore_color.rgb = CARD_BG
    c9_l.line.color.rgb = RGBColor(239, 68, 68)
    tf9_l = c9_l.text_frame
    tf9_l.word_wrap = True
    tf9_l.text = "Árbol Canónico (Filtro Tardío)"
    tf9_l.paragraphs[0].font.size = Pt(15)
    tf9_l.paragraphs[0].font.bold = True
    tf9_l.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    tree_bad = (
        "π (nombre_producto, total_vendido)\n"
        "                  |\n"
        "        γ (SUM por producto)\n"
        "                  |\n"
        "     σ (fecha = HOY)   ← SELECCIÓN AL FINAL\n"
        "                  |\n"
        "           ⋈ JOIN (id_producto)\n"
        "          /               \\\n"
        "    variante_producto    producto\n"
        "          |\n"
        "    ⋈ JOIN (id_variante)\n"
        "   /              \\\n"
        "detalle_venta   variante_producto\n"
        "      |\n"
        " ⋈ JOIN (id_venta)\n"
        " /            \\\n"
        "venta     detalle_venta\n\n"
        "Costo: Computa uniones sobre todo el histórico antes de filtrar por fecha."
    )
    p_tb = tf9_l.add_paragraph()
    p_tb.text = tree_bad
    p_tb.font.size = Pt(10)
    p_tb.font.color.rgb = TEXT_MUTED

    c9_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c9_r.fill.solid()
    c9_r.fill.fore_color.rgb = CARD_BG
    c9_r.line.color.rgb = RGBColor(34, 197, 94)
    tf9_r = c9_r.text_frame
    tf9_r.word_wrap = True
    tf9_r.text = "Árbol Optimizado con Push-Down"
    tf9_r.paragraphs[0].font.size = Pt(15)
    tf9_r.paragraphs[0].font.bold = True
    tf9_r.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    tree_good = (
        "π (nombre_producto, total_vendido)\n"
        "                  |\n"
        "        γ (SUM por producto)\n"
        "                  |\n"
        "           ⋈ JOIN (id_producto)\n"
        "          /               \\\n"
        "    variante_producto    producto\n"
        "          |\n"
        "    ⋈ JOIN (id_variante)\n"
        "   /              \\\n"
        "detalle_venta   variante_producto\n"
        "      |\n"
        " ⋈ JOIN (id_venta)\n"
        " /                          \\\n"
        "σ (fecha = HOY)          detalle_venta\n"
        " |\n"
        "venta  ← SELECCIÓN DESCENDIDA A LA HOJA\n\n"
        "Beneficio: Minimiza la cardinalidad de tuplas intermedias antes de cada JOIN, reduciendo memoria y tiempo."
    )
    p_tg = tf9_r.add_paragraph()
    p_tg.text = tree_good
    p_tg.font.size = Pt(10)
    p_tg.font.color.rgb = TEXT_MUTED

    set_notes(s9, 'GUION HABLADO (Lucas Duarte):\n"Implementamos 6 consultas complejas con agrupaciones y uniones múltiples. Para evaluar formalmente la consulta de recaudación diaria por producto, modelamos su Árbol de Álgebra Relacional y analizamos su optimización:\n\n• En el Árbol Canónico o No Optimizado, se computan sucesivamente las reuniones naturales (JOINs) de todas las tuplas históricas de "venta", "detalle_venta", "variante" y "producto", y recién en el nodo superior se aplica la selección sigma (fecha = fecha_actual). Esta aproximación es computacionalmente ineficiente debido a la gran cardinalidad de los conjuntos intermedios generados.\n\n• En el Árbol Optimizado, aplicamos la heurística formal de Push-Down de Selecciones: conmutar el operador de selección sigma descendiéndolo a través del árbol hasta alcanzar la relación base "venta". Al filtrar las ventas del día previo a la operación de Join, la cardinalidad de tuplas intermedias se reduce en varios órdenes de magnitud, optimizando el uso de memoria de trabajo (work_mem) y reduciendo el tiempo de procesamiento en el motor."')

    # ==========================================
    # SLIDE 10: SQL DIRECTO VS ORM
    # ==========================================
    s10 = add_base_slide("Fundamentación Técnica: SQL Directo vs Abstracciones ORM", "Lucas Duarte", is_int2=True)
    c10_l = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c10_l.fill.solid()
    c10_l.fill.fore_color.rgb = CARD_BG
    c10_l.line.color.rgb = RGBColor(239, 68, 68)
    tf10_l = c10_l.text_frame
    tf10_l.word_wrap = True
    tf10_l.text = "Desventajas de los ORM en BD"
    tf10_l.paragraphs[0].font.size = Pt(16)
    tf10_l.paragraphs[0].font.bold = True
    tf10_l.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    orm_cons = [
        "Pérdida de control del plan de ejecución: sentencias SQL autogeneradas difíciles de predecir.",
        "Ocultamiento del modelo relacional subyacente bajo capas opacas de objetos.",
        "Dificultad en la gestión explícita de límites transaccionales.",
        "Consultas complejas subóptimas para análisis y reportes agregados.",
        "Enfoque no recomendable para demostrar dominio riguroso del estándar SQL."
    ]
    for c in orm_cons:
        p = tf10_l.add_paragraph()
        p.text = "• " + c
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c10_r = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c10_r.fill.solid()
    c10_r.fill.fore_color.rgb = CARD_BG
    c10_r.line.color.rgb = RGBColor(34, 197, 94)
    tf10_r = c10_r.text_frame
    tf10_r.word_wrap = True
    tf10_r.text = "Garantías de SQL Directo (psycopg2)"
    tf10_r.paragraphs[0].font.size = Pt(16)
    tf10_r.paragraphs[0].font.bold = True
    tf10_r.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    psy_pros = [
        "Control absoluto de transacciones ACID: Delimitación explícita mediante bloques BEGIN, COMMIT y ROLLBACK.",
        "Transparencia en el plan de ejecución: Visualización y afinamiento directo de consultas procesadas por el optimizador.",
        "Uso de SQL parametrizado directo: Optimiza el reuso del plan de ejecución y neutraliza riesgos de inyección SQL.",
        "Manejo fino de transacciones y estados de aislamiento.",
        "Cero sobrecarga de traducción relacional-objeto."
    ]
    for p in psy_pros:
        p_node = tf10_r.add_paragraph()
        p_node.text = "• " + p
        p_node.font.size = Pt(13)
        p_node.font.color.rgb = TEXT_WHITE

    set_notes(s10, 'GUION HABLADO (Lucas Duarte):\n"Una decisión clave de arquitectura fue prescindir de un ORM y ejecutar sentencias SQL puras mediante psycopg2. Fundamentamos esta elección en principios propios de la disciplina:\n\n1. Control absoluto de transacciones ACID: Administramos de forma explícita los límites transaccionales mediante bloques BEGIN, COMMIT y ROLLBACK ante excepciones, asegurando atomicidad y durabilidad completas.\n2. Transparencia en el plan de ejecución: Los ORM generan sentencias autogeneradas que a menudo ocultan planes subóptimos o lecturas anidadas indeseadas. Con SQL directo garantizamos visibilidad total del plan que procesa el optimizador.\n3. Uso de SQL parametrizado directo: Empleamos paso de argumentos por parámetros para optimizar la reutilización del plan de ejecución en el motor y eliminar cualquier riesgo de inyección SQL."')

    # ==========================================
    # SLIDE 11: INTERFAZ COMO CONSUMIDOR TRANSACCIONAL
    # ==========================================
    s11 = add_base_slide("Interfaz de Acceso a Datos y Gestión de Transacciones", "Lucas Duarte", is_int2=True)
    c11_l = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c11_l.fill.solid()
    c11_l.fill.fore_color.rgb = CARD_BG
    c11_l.line.color.rgb = ACCENT_INDIGO
    tf11_l = c11_l.text_frame
    tf11_l.word_wrap = True
    tf11_l.text = "Control Transaccional en Punto de Venta"
    tf11_l.paragraphs[0].font.size = Pt(16)
    tf11_l.paragraphs[0].font.bold = True
    tf11_l.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    pos_features = [
        "Módulo operativo de captura de pedidos.",
        "Mecanismo de Verificación Previa al COMMIT:",
        "  - La interfaz consolida los renglones, cálculo de recargos y montos antes de emitir la transacción.",
        "  - Previene transacciones erróneas en el motor que requerirían posteriores transacciones de compensación (anulaciones o devoluciones).",
        "  - Garantiza atomicidad en la inserción de cabecera y detalles."
    ]
    for pf in pos_features:
        p = tf11_l.add_paragraph()
        p.text = "• " + pf if not pf.startswith("  -") else pf
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c11_r = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c11_r.fill.solid()
    c11_r.fill.fore_color.rgb = CARD_BG
    c11_r.line.color.rgb = ACCENT_CYAN
    tf11_r = c11_r.text_frame
    tf11_r.word_wrap = True
    tf11_r.text = "Visualización de Consultas Analíticas"
    tf11_r.paragraphs[0].font.size = Pt(16)
    tf11_r.paragraphs[0].font.bold = True
    tf11_r.paragraphs[0].font.color.rgb = ACCENT_CYAN

    dash_features = [
        "Consumo en tiempo real de consultas analíticas agregadas (SUM, COUNT, GROUP BY).",
        "Visualización interactiva de saldos de inventario crítico y productos bajo stock mínimo.",
        "Auditoría visual de recaudación y flujo comercial.",
        "Valor agregado que evidencia cómo una base de datos en 3FN soporta lecturas concurrentes sin bloqueos innecesarios."
    ]
    for df in dash_features:
        p = tf11_r.add_paragraph()
        p.text = "• " + df if not df.startswith("  -") else df
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s11, 'GUION HABLADO (Lucas Duarte):\n"Como valor agregado para la gestión operativa, desarrollamos una Interfaz de Acceso a Datos que funciona estrictamente como cliente de las transacciones del motor:\n\n• En el Punto de Venta: Diseñamos un flujo de verificación previa. Antes de emitir el comando transaccional hacia PostgreSQL, el usuario visualiza una confirmación que consolida los ítems calculados. Esto previene el envío de transacciones erróneas que exigirían posteriores transacciones compensatorias de anulación o devolución en la base de datos.\n\n• En el Módulo de Monitoreo: La interfaz consume consultas agregadas optimizadas que leen en tiempo real métricas de inventario crítico y ventas diarias, demostrando cómo una visualización clara depende directamente de una base de datos normalizada y consultas indexadas eficientes."')

    # ==========================================
    # SLIDE 12: METODOLOGÍA Y ROL ASISTENCIAL DE LA IA
    # ==========================================
    s12 = add_base_slide("Metodología de Diseño y Rol Asistencial de la IA", "Lucas Duarte", is_int2=True)
    c12_steps = [
        ("Fase 1: Modelado Conceptual Humano", "Diseño del DER, cardinalidades y normalización formal en 3FN definidos íntegramente por los autores.", Inches(0.8), Inches(1.9)),
        ("Fase 2: Asistencia Mecánica en DDL", "La IA se empleó únicamente como copiloto para acelerar el tipeo del DDL y sentencias repetitivas.", Inches(6.8), Inches(1.9)),
        ("Fase 3: Lógica Procedural y Reglas ACID", "Definición manual de funciones PL/pgSQL, triggers y transacciones parametrizadas.", Inches(0.8), Inches(3.5)),
        ("Fase 4: Formulación de Consultas Complejas", "Planteo algebraico y optimización formal con push-down de selecciones.", Inches(6.8), Inches(3.5)),
        ("Fase 5: Validación y Auditoría de Integridad", "Pruebas de consistencia de datos, verificación de claves foráneas compuestas y control transaccional.", Inches(0.8), Inches(5.1))
    ]
    for title, desc, l_pos, t_pos in c12_steps:
        w_len = Inches(11.7) if t_pos == Inches(5.1) else Inches(5.6)
        c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, t_pos, w_len, Inches(1.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = ACCENT_INDIGO
        tf = c.text_frame
        tf.word_wrap = True
        tf.text = title
        tf.paragraphs[0].font.size = Pt(14)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = ACCENT_CYAN
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED

    set_notes(s12, 'GUION HABLADO (Lucas Duarte):\n"Respecto a la metodología de desarrollo, aplicamos un protocolo estructurado por fases donde la Inteligencia Artificial cumplió un rol secundario y acotado:\n\nQueremos enfatizar que el diseño conceptual, la elaboración del Diagrama Entidad-Relación, la aplicación formal de la Tercera Forma Normal, la definición de claves compuestas y la formulación de expresiones de Álgebra Relacional fueron concebidos, calculados y validados íntegramente por nosotros como autores del proyecto.\n\nLa herramienta de IA actuó únicamente como un asistente mecánico de apoyo para agilizar el tipeo del código DDL extenso y el boilerplate de conexión, manteniendo el equipo el control técnico y decisional en cada etapa del desarrollo."')

    # ==========================================
    # SLIDE 13: CONCLUSIONES
    # ==========================================
    s13 = add_base_slide("Conclusiones Académicas y Cierre", "Lucas Duarte", is_int2=True)
    c13_l = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.0))
    c13_l.fill.solid()
    c13_l.fill.fore_color.rgb = CARD_BG
    c13_l.line.color.rgb = RGBColor(34, 197, 94)
    tf13_l = c13_l.text_frame
    tf13_l.word_wrap = True
    tf13_l.text = "Resultados del Modelo Relacional"
    tf13_l.paragraphs[0].font.size = Pt(16)
    tf13_l.paragraphs[0].font.bold = True
    tf13_l.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    achievements = [
        "Esquema de 13 tablas relacionales en 3FN libre de redundancias y anomalías.",
        "Integridad protegida a nivel motor mediante triggers en PL/pgSQL y claves compuestas.",
        "Optimización demostrable en álgebra relacional mediante la heurística de push-down.",
        "Control transaccional estricto bajo el estándar SQL sin dependencias de ORMs."
    ]
    for ac in achievements:
        p = tf13_l.add_paragraph()
        p.text = "• " + ac
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c13_r = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.0))
    c13_r.fill.solid()
    c13_r.fill.fore_color.rgb = CARD_BG
    c13_r.line.color.rgb = ACCENT_INDIGO
    tf13_r = c13_r.text_frame
    tf13_r.word_wrap = True
    tf13_r.text = "Lecciones de la Disciplina"
    tf13_r.paragraphs[0].font.size = Pt(16)
    tf13_r.paragraphs[0].font.bold = True
    tf13_r.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    lessons = [
        "La robustez de los datos debe residir en el SGBD y no delegarse a la aplicación.",
        "La normalización es un fundamento de ingeniería que previene inconsistencias críticas.",
        "El análisis formal de consultas optimiza el uso de recursos y memoria en el motor.",
        "El dominio de SQL puro otorga soberanía sobre el rendimiento transaccional."
    ]
    for ls in lessons:
        p = tf13_r.add_paragraph()
        p.text = "• " + ls
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c13_foot = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8))
    c13_foot.fill.solid()
    c13_foot.fill.fore_color.rgb = CARD_BG
    c13_foot.line.color.rgb = ACCENT_CYAN
    tf13_f = c13_foot.text_frame
    tf13_f.word_wrap = True
    p_end = tf13_f.paragraphs[0]
    p_end.text = "¡Muchas gracias por su atención! — Quedamos a disposición para las preguntas de la cátedra."
    p_end.font.size = Pt(15)
    p_end.font.bold = True
    p_end.font.color.rgb = ACCENT_CYAN
    p_end.alignment = PP_ALIGN.CENTER

    set_notes(s13, 'GUION HABLADO (Lucas Duarte):\n"Para concluir la defensa del proyecto, destacamos las siguientes conclusiones técnicas:\n\n1. Demostramos que la robustez y consistencia de un sistema no debe depender del software de aplicación, sino de las garantías formales que provee el motor relacional mediante esquemas normalizados, triggers y constraints de clave foránea compuesta.\n2. La normalización en 3FN y las técnicas de optimización en Álgebra Relacional como el push-down de selecciones no son conceptos teóricos abstractos, sino fundamentos de ingeniería indispensables para el rendimiento y la escalabilidad de bases de datos relacionales.\n3. El control explícito sobre las transacciones y consultas garantiza previsibilidad y rigor en el comportamiento del sistema.\n\nAgradecemos a la cátedra por su atención y quedamos a su entera disposición para responder las preguntas sobre el proyecto."')

    # Guardar
    output_path = "Presentacion_Marroquineria.pptx"
    prs.save(output_path)
    print(f"Academic Presentation PPTX saved to: {output_path}")

if __name__ == "__main__":
    create_academic_presentation()
