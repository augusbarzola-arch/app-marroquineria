import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_COLOR = RGBColor(15, 23, 42)        # #0f172a
    CARD_BG = RGBColor(30, 41, 59)         # #1e293b
    CARD_BORDER = RGBColor(51, 65, 85)     # #334155
    ACCENT_CYAN = RGBColor(56, 189, 248)   # #38bdf8 (Augusto)
    ACCENT_INDIGO = RGBColor(129, 140, 248)# #818cf8 (Lucas)
    TEXT_WHITE = RGBColor(248, 250, 252)   # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94a3b8
    CODE_BG = RGBColor(2, 6, 23)           # #020617

    def add_base_slide(title_text, speaker_name, is_int2=False):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

        # Top banner / Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.4), Inches(0.42))
        badge.fill.solid()
        badge.fill.fore_color.rgb = CARD_BG
        badge.line.color.rgb = ACCENT_INDIGO if is_int2 else ACCENT_CYAN
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = f"🎤 {speaker_name}"
        p_b.font.size = Pt(13)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_INDIGO if is_int2 else ACCENT_CYAN
        p_b.alignment = PP_ALIGN.CENTER

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        return slide

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================
    # SLIDE 1: PORTADA (Augusto Barzola)
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
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN
    p1.alignment = PP_ALIGN.CENTER

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Diseño, Implementación y Optimización de una Base de Datos Relacional"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = TEXT_MUTED
    p1_sub.alignment = PP_ALIGN.CENTER

    p1_space = tf1.add_paragraph()
    p1_space.text = "\nProyecto Final — Bases de Datos\n"
    p1_space.font.size = Pt(16)
    p1_space.font.color.rgb = ACCENT_INDIGO
    p1_space.alignment = PP_ALIGN.CENTER

    p1_authors = tf1.add_paragraph()
    p1_authors.text = "Disertantes (División 50/50):\nAugusto Barzola (Parte 1: Slides 1-7)  •  Lucas Duarte (Parte 2: Slides 8-13)"
    p1_authors.font.size = Pt(18)
    p1_authors.font.bold = True
    p1_authors.font.color.rgb = TEXT_WHITE
    p1_authors.alignment = PP_ALIGN.CENTER

    set_notes(s1, 'GUION HABLADO (Augusto Barzola):\n"Buenos días / buenas tardes profesor y compañeros. Somos Augusto Barzola y Lucas Duarte, y hoy les vamos a presentar nuestro proyecto final para la materia Bases de Datos.\n\nEl sistema se titula Sistema de Gestión Integral para Marroquinería: una solución Full Stack construida desde el diseño formal relacional en PostgreSQL, backend en Python con FastAPI y psycopg2, y una interfaz web moderna en modo oscuro con glassmorphism.\n\nEn los próximos minutos vamos a mostrar cómo la base de datos garantiza por sí misma la integridad del negocio y cómo optimizamos las consultas más exigentes."')

    # ==========================================
    # SLIDE 2: AGENDA (Augusto Barzola)
    # ==========================================
    s2 = add_base_slide("¿Qué vamos a ver hoy? — Agenda", "Augusto Barzola")
    c2_1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c2_1.fill.solid()
    c2_1.fill.fore_color.rgb = CARD_BG
    c2_1.line.color.rgb = ACCENT_CYAN
    tf2_1 = c2_1.text_frame
    tf2_1.word_wrap = True
    tf2_1.text = "Bloque I — Augusto Barzola (Slides 1 a 7)"
    tf2_1.paragraphs[0].font.size = Pt(17)
    tf2_1.paragraphs[0].font.bold = True
    tf2_1.paragraphs[0].font.color.rgb = ACCENT_CYAN

    items_b1 = [
        "1. Descripción del problema y la solución",
        "2. Arquitectura del sistema (Stack tecnológico)",
        "3. Modelo de datos — DER (13 tablas normalizadas)",
        "4. Normalización en Tercera Forma Normal (3FN)",
        "5. Triggers de stock en base de datos (PL/pgSQL)",
        "6. Control atómico de inventario"
    ]
    for it in items_b1:
        p = tf2_1.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    c2_2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c2_2.fill.solid()
    c2_2.fill.fore_color.rgb = CARD_BG
    c2_2.line.color.rgb = ACCENT_INDIGO
    tf2_2 = c2_2.text_frame
    tf2_2.word_wrap = True
    tf2_2.text = "Bloque II — Lucas Duarte (Slides 8 a 13)"
    tf2_2.paragraphs[0].font.size = Pt(17)
    tf2_2.paragraphs[0].font.bold = True
    tf2_2.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    items_b2 = [
        "8. Integridad en Devoluciones (FK compuesta)",
        "9. Consultas complejas y Álgebra Relacional (Push-Down)",
        "10. Decisión técnica: SQL directo (psycopg2) vs ORM",
        "11. Demostración UI/UX: POS Modal y Dashboard",
        "12. Metodología de desarrollo asistido con IA",
        "13. Conclusiones y lecciones aprendidas"
    ]
    for it in items_b2:
        p = tf2_2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s2, 'GUION HABLADO (Augusto Barzola):\n"Esta es la hoja de ruta de la presentación. Dividimos la exposición exactamente en dos bloques continuos: yo voy a cubrir la descripción del problema, la arquitectura, el modelo relacional en 3FN y los triggers de stock en PostgreSQL; y Lucas continuará con la integridad en devoluciones con clave foránea compuesta, la optimización matemática con álgebra relacional, la interfaz y las conclusiones."')

    # ==========================================
    # SLIDE 3: PROBLEMA Y SOLUCION (Augusto Barzola)
    # ==========================================
    s3 = add_base_slide("El Problema de Negocio y Nuestra Solución", "Augusto Barzola")
    c3_1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c3_1.fill.solid()
    c3_1.fill.fore_color.rgb = CARD_BG
    c3_1.line.color.rgb = RGBColor(239, 68, 68)
    tf3_1 = c3_1.text_frame
    tf3_1.word_wrap = True
    tf3_1.text = "❌ El Problema en la PYME"
    tf3_1.paragraphs[0].font.size = Pt(18)
    tf3_1.paragraphs[0].font.bold = True
    tf3_1.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    prob_items = [
        "Gestión manual de stock en planillas Excel o cuadernos.",
        "Mercadería perdida, descuadres y roturas de stock no detectadas.",
        "Devoluciones no controladas con inconsistencias contables.",
        "Imposibilidad de conocer las ventas del día o productos estrella en tiempo real.",
        "Complejidad intrínseca: un producto tiene múltiples variantes (color, material, tamaño)."
    ]
    for it in prob_items:
        p = tf3_1.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    c3_2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    c3_2.fill.solid()
    c3_2.fill.fore_color.rgb = CARD_BG
    c3_2.line.color.rgb = RGBColor(34, 197, 94)
    tf3_2 = c3_2.text_frame
    tf3_2.word_wrap = True
    tf3_2.text = "✅ Nuestra Solución Full Stack"
    tf3_2.paragraphs[0].font.size = Pt(18)
    tf3_2.paragraphs[0].font.bold = True
    tf3_2.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    sol_items = [
        "Base de datos PostgreSQL centralizada con 13 tablas normalizadas en 3FN.",
        "Integridad protegida a nivel de motor (Triggers y Foreign Keys compuestas).",
        "Módulo POS ágil con modal de confirmación tipo ticket fiscal.",
        "Dashboard gerencial en tiempo real con tarjetas expandibles.",
        "Historial auditable de movimientos de compra, venta y devolución."
    ]
    for it in sol_items:
        p = tf3_2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s3, 'GUION HABLADO (Augusto Barzola):\n"Para contextualizar el negocio: una marroquinería vende artículos de cuero con variantes de color, material y tamaño. En la PYME promedio, el control se lleva en cuadernos o planillas de cálculo, generando descuadres de inventario y devoluciones no controladas.\n\nNuestra solución fue construir un sistema de gestión integral centralizado en PostgreSQL, donde la base de datos es la única fuente de verdad: el motor protege su propia información con triggers y restricciones estrictas, brindándole al comerciante un Punto de Venta ágil y un Dashboard analítico en tiempo real."')

    # ==========================================
    # SLIDE 4: ARQUITECTURA (Augusto Barzola)
    # ==========================================
    s4 = add_base_slide("Arquitectura del Sistema — Stack Tecnológico", "Augusto Barzola")
    c4_left = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(6.5), Inches(4.8))
    c4_left.fill.solid()
    c4_left.fill.fore_color.rgb = CARD_BG
    c4_left.line.color.rgb = CARD_BORDER
    tf4_l = c4_left.text_frame
    tf4_l.word_wrap = True
    tf4_l.text = "Capas del Sistema"
    tf4_l.paragraphs[0].font.size = Pt(18)
    tf4_l.paragraphs[0].font.bold = True
    tf4_l.paragraphs[0].font.color.rgb = ACCENT_CYAN

    arch_bullets = [
        "Base de Datos (PostgreSQL): 13 tablas, integridad referencial estricta, triggers PL/pgSQL y constraints.",
        "Backend (FastAPI - Python): API REST asíncrona de alto desempeño, tipado con Pydantic y documentación OpenAPI.",
        "Conector BD (psycopg2): Conexión directa sin ORM mediante ThreadedConnectionPool.",
        "Frontend (Jinja2 + Bootstrap 5): Renderizado server-side reactivo con estilos personalizados en Glassmorphism y Dark Mode."
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
    tf4_r.text = "Flujo de Comunicación\n\n"
    tf4_r.paragraphs[0].font.size = Pt(16)
    tf4_r.paragraphs[0].font.bold = True
    tf4_r.paragraphs[0].font.color.rgb = ACCENT_CYAN

    diagram_text = (
        "[ Frontend Web ]\n"
        "Jinja2 + Bootstrap 5 + JS\n"
        "       ↕  (HTTP / HTML / JSON)\n\n"
        "[ Backend REST API ]\n"
        "FastAPI (Python 3.11)\n"
        "       ↕  (psycopg2 Connection Pool)\n\n"
        "[ Motor Relacional ]\n"
        "PostgreSQL (13 Tablas + Triggers)"
    )
    p_diag = tf4_r.add_paragraph()
    p_diag.text = diagram_text
    p_diag.font.size = Pt(13)
    p_diag.font.color.rgb = TEXT_WHITE

    set_notes(s4, 'GUION HABLADO (Augusto Barzola):\n"La arquitectura del sistema sigue un modelo por capas limpio y desacoplado: en la base tenemos PostgreSQL como motor relacional con sus 13 tablas y triggers; por encima, el backend en Python con FastAPI por su rendimiento asíncrono y tipado estricto.\n\nPara comunicarnos con la base usamos psycopg2 directo con ThreadedConnectionPool, y en la capa visual Jinja2 con Bootstrap 5 en modo oscuro con glassmorphism. Es una estructura pensada para ser robusta y eficiente sin capas de abstracción innecesarias."')

    # ==========================================
    # SLIDE 5: DER (Augusto Barzola)
    # ==========================================
    s5 = add_base_slide("Modelo de Datos — Diagrama Entidad-Relación (13 Tablas)", "Augusto Barzola")
    der_cats = [
        ("Entidades Principales", "producto\nvariante_producto\nventa\ncompra", Inches(0.8), ACCENT_CYAN),
        ("Detalles Transaccionales", "detalle_venta\ndetalle_compra\ndevolucion", Inches(4.8), ACCENT_INDIGO),
        ("Tablas de Dominio", "categoria\nmaterial\ncolor\ntamano\nproveedor\nmedio_pago", Inches(8.8), RGBColor(34, 197, 94))
    ]
    for title, tbls, left_pos, col in der_cats:
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(3.7), Inches(3.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        tf = c.text_frame
        tf.word_wrap = True
        tf.text = title
        tf.paragraphs[0].font.size = Pt(16)
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
    p_b1.text = "• Claves primarias compuestas: (id_venta, renglon_venta) y (id_compra, renglon_compra)."
    p_b1.font.size = Pt(12)
    p_b1.font.color.rgb = TEXT_MUTED
    p_b2 = tf5_b.add_paragraph()
    p_b2.text = "• Constraints CHECK (cantidad > 0, precio > 0) y restricciones NOT NULL en campos transaccionales."
    p_b2.font.size = Pt(12)
    p_b2.font.color.rgb = TEXT_MUTED

    set_notes(s5, 'GUION HABLADO (Augusto Barzola):\n"El modelo relacional consta de 13 tablas organizadas en tres categorías: entidades maestras (producto, variante, venta, compra), tablas de detalle (detalle_venta, detalle_compra, devolucion) y tablas de dominio (categoria, material, color, tamaño, proveedor, medio de pago).\n\nUn rasgo técnico clave es el uso de Claves Primarias Compuestas en las tablas de detalle, como (id_venta, renglon_venta), garantizando que dentro de un comprobante cada renglón es único e irrepetible. Cada relación está protegida por Foreign Keys que impiden registros huérfanos."')

    # ==========================================
    # SLIDE 6: 3FN (Augusto Barzola)
    # ==========================================
    s6 = add_base_slide("Normalización en Tercera Forma Normal (3FN)", "Augusto Barzola")
    c6_top = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.7), Inches(2.2))
    c6_top.fill.solid()
    c6_top.fill.fore_color.rgb = CARD_BG
    c6_top.line.color.rgb = CARD_BORDER
    tf6_t = c6_top.text_frame
    tf6_t.word_wrap = True
    tf6_t.text = "Cumplimiento Formal de las Formas Normales"
    tf6_t.paragraphs[0].font.size = Pt(16)
    tf6_t.paragraphs[0].font.bold = True
    tf6_t.paragraphs[0].font.color.rgb = ACCENT_CYAN

    fn_rules = [
        "1FN (Primera Forma Normal): Atributos atómicos; sin campos multivaluados ni listas repetitivas.",
        "2FN (Segunda Forma Normal): Todo atributo no-clave depende de la totalidad de la clave primaria (sin dependencia parcial).",
        "3FN (Tercera Forma Normal): Sin dependencias transitivas (ningún atributo no-clave depende de otro atributo no-clave)."
    ]
    for r in fn_rules:
        p = tf6_t.add_paragraph()
        p.text = "• " + r
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    c6_bad = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5))
    c6_bad.fill.solid()
    c6_bad.fill.fore_color.rgb = CARD_BG
    c6_bad.line.color.rgb = RGBColor(239, 68, 68)
    tf6_bad = c6_bad.text_frame
    tf6_bad.word_wrap = True
    tf6_bad.text = "❌ Sin 3FN (Diseño Deficiente)"
    tf6_bad.paragraphs[0].font.size = Pt(15)
    tf6_bad.paragraphs[0].font.bold = True
    tf6_bad.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)
    p_b_text = tf6_bad.add_paragraph()
    p_b_text.text = "variante_producto(\n  id_variante,\n  color='Negro',\n  material='Cuero Vacuno'\n)\n\nProblema: Modificar el nombre del color exige un UPDATE masivo en miles de filas."
    p_b_text.font.size = Pt(12)
    p_b_text.font.color.rgb = TEXT_MUTED

    c6_good = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5))
    c6_good.fill.solid()
    c6_good.fill.fore_color.rgb = CARD_BG
    c6_good.line.color.rgb = RGBColor(34, 197, 94)
    tf6_good = c6_good.text_frame
    tf6_good.word_wrap = True
    tf6_good.text = "✅ Con 3FN (Diseño del Proyecto)"
    tf6_good.paragraphs[0].font.size = Pt(15)
    tf6_good.paragraphs[0].font.bold = True
    tf6_good.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)
    p_g_text = tf6_good.add_paragraph()
    p_g_text.text = "variante_producto(id_variante, id_color, id_material)\ncolor(id_color, nombre_color)\n\nBeneficio: Cero anomalías de inserción, actualización o borrado. El color se define UNA sola vez."
    p_g_text.font.size = Pt(12)
    p_g_text.font.color.rgb = TEXT_MUTED

    set_notes(s6, 'GUION HABLADO (Augusto Barzola):\n"El modelo cumple rigurosamente con la Tercera Forma Normal (3FN): atributos atómicos, dependencia funcional completa y erradicación de dependencias transitivas.\n\nEjemplo práctico: en lugar de guardar el color como texto en variante_producto, creamos la tabla satélite color y relacionamos su ID. Si el negocio decide renombrar un color, se ejecuta un único UPDATE en una sola fila, preservando la consistencia absoluta del historial sin anomalías de actualización."')

    # ==========================================
    # SLIDE 7: TRIGGERS (Augusto Barzola)
    # ==========================================
    s7 = add_base_slide("Triggers — La Base de Datos se Protege a Sí Misma", "Augusto Barzola")
    c7_left = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.8))
    c7_left.fill.solid()
    c7_left.fill.fore_color.rgb = CARD_BG
    c7_left.line.color.rgb = ACCENT_CYAN
    tf7_l = c7_left.text_frame
    tf7_l.word_wrap = True
    tf7_l.text = "Lógica Transaccional de Stock"
    tf7_l.paragraphs[0].font.size = Pt(16)
    tf7_l.paragraphs[0].font.bold = True
    tf7_l.paragraphs[0].font.color.rgb = ACCENT_CYAN

    trg_points = [
        "El stock se actualiza AUTOMÁTICAMENTE a nivel de motor SQL.",
        "detalle_venta INSERT → Trigger RESTA de forma atómica stock_actual en variante_producto.",
        "detalle_compra INSERT → Trigger SUMA stock_actual al ingresar mercadería.",
        "Independencia de la aplicación: si se inserta desde pgAdmin, scripts o migración, el trigger se dispara de igual manera.",
        "NEW.cantidad contiene el valor de la fila recién insertada en PL/pgSQL."
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
    tf7_r.text = "Código PL/pgSQL Implementado:\n"
    tf7_r.paragraphs[0].font.size = Pt(14)
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

    set_notes(s7, 'GUION HABLADO (Augusto Barzola):\n"Para cerrar mi parte, quiero explicar los Triggers en PostgreSQL: la actualización de stock NO se delega al frontend ni al backend. Al insertar en detalle_venta, el trigger decrementa el stock_actual automáticamente; y al ingresar compras, lo incrementa.\n\nEsto garantiza que incluso si alguien inserta registros por consola desde pgAdmin, el trigger se dispara igual. NEW.cantidad captura el valor recién insertado en PL/pgSQL.\n\n[TRANSICIÓN CLAVE]: Habiendo visto la base de datos y sus triggers, le paso la palabra a Lucas para que continúe con la integridad en devoluciones, el álgebra relacional, la interfaz y las conclusiones."')

    # ==========================================
    # SLIDE 8: TABLA DEVOLUCION (Lucas Duarte)
    # ==========================================
    s8 = add_base_slide("Tabla Devolución — Integridad con Foreign Key Compuesta", "Lucas Duarte", is_int2=True)
    c8_t = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.7), Inches(1.2))
    c8_t.fill.solid()
    c8_t.fill.fore_color.rgb = CARD_BG
    c8_t.line.color.rgb = RGBColor(234, 179, 8)
    tf8_t = c8_t.text_frame
    tf8_t.word_wrap = True
    tf8_t.text = "🎯 Problema Crítico a Resolver:"
    tf8_t.paragraphs[0].font.size = Pt(15)
    tf8_t.paragraphs[0].font.bold = True
    tf8_t.paragraphs[0].font.color.rgb = RGBColor(234, 179, 8)
    p_prob = tf8_t.add_paragraph()
    p_prob.text = "¿Cómo evitar registrar una devolución de un ítem que NUNCA estuvo en esa venta?"
    p_prob.font.size = Pt(14)
    p_prob.font.color.rgb = TEXT_WHITE

    c8_code = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(6.0), Inches(3.4))
    c8_code.fill.solid()
    c8_code.fill.fore_color.rgb = CODE_BG
    c8_code.line.color.rgb = CARD_BORDER
    tf8_c = c8_code.text_frame
    tf8_c.word_wrap = True
    tf8_c.text = "Definición DDL con FK Compuesta:\n"
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
        ");"
    )
    p_dev_c = tf8_c.add_paragraph()
    p_dev_c.text = dev_ddl
    p_dev_c.font.size = Pt(11)
    p_dev_c.font.color.rgb = ACCENT_INDIGO

    c8_why = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(3.3), Inches(5.4), Inches(3.4))
    c8_why.fill.solid()
    c8_why.fill.fore_color.rgb = CARD_BG
    c8_why.line.color.rgb = ACCENT_INDIGO
    tf8_w = c8_why.text_frame
    tf8_w.word_wrap = True
    tf8_w.text = "Garantía de Integridad Estricta"
    tf8_w.paragraphs[0].font.size = Pt(15)
    tf8_w.paragraphs[0].font.bold = True
    tf8_w.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    dev_points = [
        "Una FK simple a id_venta solo verifica que la venta existe, pero NO garantiza que ese renglón/producto fue vendido.",
        "La FK compuesta (id_venta, renglon_venta) exige la coincidencia exacta de ambos atributos en detalle_venta.",
        "Si el par no existe, PostgreSQL RECHAZA físicamente el INSERT con error de Foreign Key.",
        "Elimina por completo devoluciones 'fantasma' o de otros tickets."
    ]
    for p in dev_points:
        p_w = tf8_w.add_paragraph()
        p_w.text = "• " + p
        p_w.font.size = Pt(12)
        p_w.font.color.rgb = TEXT_WHITE

    set_notes(s8, 'GUION HABLADO (Lucas Duarte):\n"Gracias Augusto. Continuando con la solidez de la base de datos, quiero destacar el diseño de la tabla devolucion, que resuelve un problema de integridad que una foreign key simple no puede solucionar.\n\nSi usáramos solo una FK a id_venta, verificaríamos que la venta existe, pero no que ese ítem en particular estuvo en esa venta.\n\nLa solución fue definir una clave foránea compuesta referenciando al par (id_venta, renglon_venta) de detalle_venta. La base de datos, antes de permitir el INSERT en devolucion, verifica que ese par exacto exista. Si no, rechaza la operación automáticamente. Es una garantía a nivel motor, sin depender de validaciones manuales de software."')

    # ==========================================
    # SLIDE 9: ALGEBRA RELACIONAL (Lucas Duarte)
    # ==========================================
    s9 = add_base_slide("Consultas Complejas y Álgebra Relacional (Push-Down)", "Lucas Duarte", is_int2=True)
    c9_l = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c9_l.fill.solid()
    c9_l.fill.fore_color.rgb = CARD_BG
    c9_l.line.color.rgb = RGBColor(239, 68, 68)
    tf9_l = c9_l.text_frame
    tf9_l.word_wrap = True
    tf9_l.text = "❌ Árbol Ingenuo (Sin Optimizar)"
    tf9_l.paragraphs[0].font.size = Pt(15)
    tf9_l.paragraphs[0].font.bold = True
    tf9_l.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    tree_bad = (
        "π (nombre_producto, total_vendido)\n"
        "                  |\n"
        "        γ (SUM por producto)\n"
        "                  |\n"
        "     σ (fecha = HOY)   ← FILTRO TARDÍO\n"
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
        "Problema: JOIN masivo de TODAS las ventas históricas antes de filtrar."
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
    tf9_r.text = "✅ Árbol Optimizado con Push-Down"
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
        "venta  ← FILTRO APLICADO EN LA HOJA\n\n"
        "Beneficio: El JOIN recibe solo 20 filas en lugar de miles. Consumo mínimo de memoria y CPU."
    )
    p_tg = tf9_r.add_paragraph()
    p_tg.text = tree_good
    p_tg.font.size = Pt(10)
    p_tg.font.color.rgb = TEXT_MUTED

    set_notes(s9, 'GUION HABLADO (Lucas Duarte):\n"Implementamos 6 consultas SQL complejas con subconsultas y múltiples JOINs. Para optimizar la consulta más costosa —recaudación del día agrupada por producto— modelamos su Árbol de Álgebra Relacional.\n\nUn árbol ingenuo realiza primero el JOIN de todas las ventas históricas con todos los detalles y recién al final aplica el filtro de fecha, saturando la memoria.\n\nAplicamos la regla formal de Push-Down de Selecciones: empujar el operador sigma (fecha = hoy) hacia las hojas del árbol, antes de los JOINs. Así, el JOIN trabaja únicamente con las 20 transacciones de hoy en vez de miles de registros históricos. Esta técnica es el principio básico de los optimizadores de bases de datos."')

    # ==========================================
    # SLIDE 10: SQL DIRECTO VS ORM (Lucas Duarte)
    # ==========================================
    s10 = add_base_slide("Decisión de Arquitectura: SQL Directo vs ORM", "Lucas Duarte", is_int2=True)
    c10_l = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c10_l.fill.solid()
    c10_l.fill.fore_color.rgb = CARD_BG
    c10_l.line.color.rgb = RGBColor(239, 68, 68)
    tf10_l = c10_l.text_frame
    tf10_l.word_wrap = True
    tf10_l.text = "Por qué NO usamos ORM"
    tf10_l.paragraphs[0].font.size = Pt(16)
    tf10_l.paragraphs[0].font.bold = True
    tf10_l.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

    orm_cons = [
        "Consultas implícitas o 'fantasma': riesgo del problema N+1 en lecturas anidadas.",
        "Oculta lo que realmente ocurre en el motor relacional.",
        "Dificulta el control granular de transacciones (BEGIN, COMMIT, ROLLBACK).",
        "Genera SQL autogenerado que suele ser subóptimo en reportes y consultas analíticas complejas.",
        "Para una cátedra de Bases de Datos, usar ORM enmascara el aprendizaje de SQL."
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
    tf10_r.text = "Por qué elegimos psycopg2"
    tf10_r.paragraphs[0].font.size = Pt(16)
    tf10_r.paragraphs[0].font.bold = True
    tf10_r.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    psy_pros = [
        "Control absoluto del plan de ejecución y sintaxis PostgreSQL.",
        "Pool de conexiones thread-safe con ThreadedConnectionPool (min=2, max=10).",
        "Transacciones explícitas gestionadas con context managers de Python.",
        "Resultados inmediatos en formato diccionario usando RealDictCursor.",
        "Cero sobrecarga de abstracción: máxima velocidad de ejecución.",
        "Transparencia total del código SQL presentado."
    ]
    for p in psy_pros:
        p_node = tf10_r.add_paragraph()
        p_node.text = "• " + p
        p_node.font.size = Pt(13)
        p_node.font.color.rgb = TEXT_WHITE

    set_notes(s10, 'GUION HABLADO (Lucas Duarte):\n"Una decisión arquitectónica importante fue prescindir de un ORM y utilizar psycopg2 de forma directa.\n\nAunque herramientas como SQLAlchemy facilitan el prototipado rápido, introducen capas de abstracción opacas, generan consultas N+1 difíciles de predecir y complican el control fino de transacciones.\n\nAl trabajar con SQL puro y psycopg2 escribimos y optimizamos cada consulta a mano, administramos transacciones explícitas con bloques BEGIN, COMMIT y ROLLBACK, y usamos ThreadedConnectionPool para gestionar conexiones concurrentes. Académicamente, demostramos dominio absoluto del estándar SQL."')

    # ==========================================
    # SLIDE 11: POS Y DASHBOARD (Lucas Duarte)
    # ==========================================
    s11 = add_base_slide("Interfaz de Usuario — Experiencia y Control de Errores", "Lucas Duarte", is_int2=True)
    c11_l = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    c11_l.fill.solid()
    c11_l.fill.fore_color.rgb = CARD_BG
    c11_l.line.color.rgb = ACCENT_INDIGO
    tf11_l = c11_l.text_frame
    tf11_l.word_wrap = True
    tf11_l.text = "Punto de Venta (POS)"
    tf11_l.paragraphs[0].font.size = Pt(16)
    tf11_l.paragraphs[0].font.bold = True
    tf11_l.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    pos_features = [
        "Búsqueda instantánea de productos con filtrado dinámico de variantes.",
        "Cálculo automático de recargos / descuentos según medio de pago.",
        "Modal de Confirmación tipo Ticket Fiscal:",
        "  - Resumen detallado: ítems, cantidades, subtotales y total final.",
        "  - El vendedor verifica antes de confirmar la transacción.",
        "  - Previene ventas erróneas y reduce devoluciones innecesarias."
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
    tf11_r.text = "Dashboard Gerencial"
    tf11_r.paragraphs[0].font.size = Pt(16)
    tf11_r.paragraphs[0].font.bold = True
    tf11_r.paragraphs[0].font.color.rgb = ACCENT_CYAN

    dash_features = [
        "Tarjetas de métricas en vivo: recaudación del día, productos bajo stock crítico, transacciones.",
        "Tarjetas Expandibles Interactivas:",
        "  - Al hacer clic en 'Stock Bajo', la tarjeta se expande con animación CSS suave y despliega la tabla con todos los productos afectados.",
        "  - Al hacer clic en 'Ventas', muestra el detalle de los últimos tickets.",
        "Diseño Glassmorphism en Dark Mode para confort visual durante jornadas operativas continuas."
    ]
    for df in dash_features:
        p = tf11_r.add_paragraph()
        p.text = "• " + df if not df.startswith("  -") else df
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    set_notes(s11, 'GUION HABLADO (Lucas Duarte):\n"Pasando a la experiencia del usuario, diseñamos dos módulos orientados a prevenir errores operativos:\n\nEn el Punto de Venta (POS), incorporamos un modal de confirmación con formato de ticket fiscal antes de guardar la venta. El usuario revisa ítems, cantidades y totales antes de disparar el commit real, eliminando errores de facturación.\n\nEn el Dashboard, presentamos tarjetas de métricas en tiempo real con tarjetas expandibles interactivas: al hacer clic en Stock Bajo, la tarjeta se despliega suavemente y muestra la tabla con todas las variantes bajo el umbral mínimo de seguridad. Todo bajo un diseño glassmorphism en modo oscuro para reducir la fatiga visual."')

    # ==========================================
    # SLIDE 12: DESARROLLO CON IA (Lucas Duarte)
    # ==========================================
    s12 = add_base_slide("Desarrollo Asistido por IA — Metodología por Fases", "Lucas Duarte", is_int2=True)
    c12_steps = [
        ("Fase 1: Modelo Conceptual", "Diseño del DER y definición de entidades en 3FN.", Inches(0.8), Inches(1.9)),
        ("Fase 2: Motor Relacional", "Script DDL, constraints CHECK/UNIQUE y triggers PL/pgSQL.", Inches(6.8), Inches(1.9)),
        ("Fase 3: Backend FastAPI", "Rutas REST, psycopg2 connection pool y manejo transaccional.", Inches(0.8), Inches(3.5)),
        ("Fase 4: Frontend Jinja2", "Plantillas HTML, Bootstrap 5, modales y tarjetas expandibles.", Inches(6.8), Inches(3.5)),
        ("Fase 5: Testing e Integración", "Validación de integridad referencial, push-down y sincronización de secuencias.", Inches(0.8), Inches(5.1))
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

    set_notes(s12, 'GUION HABLADO (Lucas Duarte):\n"En cuanto a la metodología, aplicamos desarrollo asistido por Inteligencia Artificial utilizando Antigravity de Google DeepMind bajo un estricto protocolo en 5 fases: desde el modelado conceptual y DDL en las primeras fases, pasando por el backend FastAPI y frontend Jinja2, hasta la auditoría de integridad y optimización.\n\nQueremos enfatizar que la IA operó como un co-piloto técnico que aceleró la escritura de código, pero las decisiones de arquitectura, el diseño relacional y la validación de cada línea fueron guiadas y auditadas íntegramente por nosotros."')

    # ==========================================
    # SLIDE 13: CONCLUSIONES (Lucas Duarte)
    # ==========================================
    s13 = add_base_slide("Conclusiones y Lecciones Aprendidas", "Lucas Duarte", is_int2=True)
    c13_l = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.0))
    c13_l.fill.solid()
    c13_l.fill.fore_color.rgb = CARD_BG
    c13_l.line.color.rgb = RGBColor(34, 197, 94)
    tf13_l = c13_l.text_frame
    tf13_l.word_wrap = True
    tf13_l.text = "🏆 Logros del Proyecto"
    tf13_l.paragraphs[0].font.size = Pt(16)
    tf13_l.paragraphs[0].font.bold = True
    tf13_l.paragraphs[0].font.color.rgb = RGBColor(34, 197, 94)

    achievements = [
        "Sistema Full Stack 100% funcional para un comercio real.",
        "Base de datos de 13 tablas en 3FN sin redundancias.",
        "Integridad garantizada por el motor SQL (Triggers y FK compuesta en Devoluciones).",
        "Consultas optimizadas con técnica formal de Push-Down de selecciones.",
        "Interfaz moderna, reactiva y orientada a prevenir errores operativos."
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
    tf13_r.text = "💡 Lecciones Técnicas"
    tf13_r.paragraphs[0].font.size = Pt(16)
    tf13_r.paragraphs[0].font.bold = True
    tf13_r.paragraphs[0].font.color.rgb = ACCENT_INDIGO

    lessons = [
        "La normalización no es teoría académica: previene bugs costosos en producción.",
        "Los triggers son la última línea de defensa de la verdad de los datos.",
        "Elegir SQL directo con psycopg2 nos dio control real sobre transacciones y performance.",
        "El desarrollo asistido con IA es altamente productivo cuando se guía con criterio técnico."
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
    p_end.text = "¡Muchas gracias por su atención! — ¿Preguntas de la cátedra?"
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = ACCENT_CYAN
    p_end.alignment = PP_ALIGN.CENTER

    set_notes(s13, 'GUION HABLADO (Lucas Duarte):\n"Para concluir, queremos sintetizar los logros del proyecto: entregamos un software Full Stack completamente operativo, una base de datos normalizada en 3FN y autosuficiente gracias a sus triggers y claves foráneas compuestas. Aprendimos que la normalización y el álgebra relacional no son meros conceptos teóricos, sino herramientas indispensables para construir software escalable.\n\nLes agradecemos mucho por su atención y quedamos a disposición de la cátedra para responder todas sus preguntas."')

    # Save presentation
    output_path = "Presentacion_Marroquineria.pptx"
    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")

if __name__ == "__main__":
    create_presentation()
