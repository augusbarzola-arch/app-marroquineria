import os
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Portada limpia sin encabezado ni pie
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Encabezado
        self.drawString(54, 11 * inch - 36, "Trabajo Integrador Final — Cátedra de Bases de Datos | Marroquinería")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Pie de página
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "Autores: Augusto Barzola & Lucas Duarte — PostgreSQL 14+")
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.restoreState()

def clean_inline_md(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Negrita + Cursiva
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Negrita
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Cursiva
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#0369a1">\1</font>', text)
    return text

def convert_md_to_pdf(md_path, pdf_path, title_header):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15,
        spaceAfter=3
    )
    quote_style = ParagraphStyle(
        'Quote_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        leftIndent=15,
        rightIndent=15,
        spaceBefore=4,
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=0,
        spaceAfter=0
    )

    story = []

    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.rstrip("\r\n")

        # Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                # Render code box as a single-cell table with background
                escaped_code = "<br/>".join([
                    l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
                    for l in code_lines
                ])
                if not escaped_code.strip():
                    escaped_code = "&nbsp;"
                p_code = Paragraph(f"<font face='Courier' size='7.5'>{escaped_code}</font>", code_style)
                code_table = Table([[p_code]], colWidths=[7.0 * inch])
                code_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                    ('PADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]))
                story.append(code_table)
                story.append(Spacer(1, 8))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(stripped)
            continue

        # Markdown tables
        if stripped.startswith("|") and stripped.endswith("|"):
            # Header separator line |---|---|
            if re.match(r'^\|[\s\-:]+(\|[\s\-:]+)+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
            continue
        elif in_table:
            # End of table, render it
            if table_rows:
                num_cols = len(table_rows[0])
                col_w = (7.0 * inch) / max(num_cols, 1)
                t_data = []
                for r_idx, r in enumerate(table_rows):
                    row_cells = []
                    for c_idx, c in enumerate(r):
                        is_hdr = (r_idx == 0)
                        fn = 'Helvetica-Bold' if is_hdr else 'Helvetica'
                        fs = 8.5 if is_hdr else 8
                        tc = colors.HexColor("#ffffff") if is_hdr else colors.HexColor("#1e293b")
                        p_cell = Paragraph(
                            f"<font color='{tc.hexval()}'>{clean_inline_md(c)}</font>",
                            ParagraphStyle('CellP', fontName=fn, fontSize=fs, leading=10.5)
                        )
                        row_cells.append(p_cell)
                    t_data.append(row_cells)
                
                md_table = Table(t_data, colWidths=[col_w]*num_cols)
                t_style = [
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                    ('PADDING', (0,0), (-1,-1), 5),
                ]
                for r_i in range(1, len(table_rows)):
                    if r_i % 2 == 1:
                        t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), colors.HexColor("#f8fafc")))
                md_table.setStyle(TableStyle(t_style))
                story.append(md_table)
                story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        if not stripped:
            continue

        # Encabezados
        if stripped.startswith("# "):
            h_text = clean_inline_md(stripped[2:])
            story.append(Paragraph(h_text, title_style))
            story.append(Spacer(1, 4))
        elif stripped.startswith("## "):
            h_text = clean_inline_md(stripped[3:])
            story.append(Paragraph(h_text, h1_style))
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#0369a1"), spaceAfter=8))
        elif stripped.startswith("### "):
            h_text = clean_inline_md(stripped[4:])
            story.append(Paragraph(h_text, h2_style))
        elif stripped.startswith("#### "):
            h_text = clean_inline_md(stripped[5:])
            story.append(Paragraph(h_text, h3_style))
        elif stripped.startswith("> "):
            q_text = clean_inline_md(stripped[2:])
            # Bloque de cita o diálogo
            p_q = Paragraph(q_text, quote_style)
            q_table = Table([[p_q]], colWidths=[7.0 * inch])
            q_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
                ('LINELEFT', (0,0), (-1,-1), 3, colors.HexColor("#0284c7")),
                ('PADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(q_table)
            story.append(Spacer(1, 4))
        elif stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("• "):
            bullet_text = clean_inline_md(stripped[2:])
            story.append(Paragraph(f"• &nbsp; {bullet_text}", bullet_style))
        elif re.match(r'^\d+\.\s', stripped):
            match = re.match(r'^(\d+\.)\s*(.*)', stripped)
            prefix = match.group(1)
            content = clean_inline_md(match.group(2))
            story.append(Paragraph(f"<b>{prefix}</b> {content}", bullet_style))
        elif stripped == "---":
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
        else:
            p_text = clean_inline_md(stripped)
            story.append(Paragraph(p_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito: {pdf_path}")

if __name__ == "__main__":
    base_dir = r"C:\Users\augus\OneDrive\Desktop\bases de datos\base-de-datos-marroquineria\Entrega_Final_TIF"
    
    # 1. Convertir Informe_TIF.md
    informe_md = os.path.join(base_dir, "Informe_TIF.md")
    informe_pdf = os.path.join(base_dir, "Informe_TIF.pdf")
    convert_md_to_pdf(informe_md, informe_pdf, "Informe Técnico TIF")

    # 2. Convertir Guion_y_Presentacion_TIF.md
    guion_md = os.path.join(base_dir, "Guion_y_Presentacion_TIF.md")
    guion_pdf = os.path.join(base_dir, "Guion_y_Presentacion_TIF.pdf")
    convert_md_to_pdf(guion_md, guion_pdf, "Guion y Presentación TIF")
