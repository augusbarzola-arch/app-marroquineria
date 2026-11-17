import csv
import io
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Tuple, Optional

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.repositories.reporte_repo import ReporteRepository


class ReporteService:
    """Servicio para formateo y exportación de reportes a CSV y PDF."""

    # =========================================================================
    # 1. GENERADORES GENÉRICOS DE EXPORTACIÓN (CSV / PDF)
    # =========================================================================

    @staticmethod
    def exportar_a_csv(columnas: List[str], filas: List[List[Any]]) -> bytes:
        """Genera un archivo CSV codificado en UTF-8 con BOM para máxima compatibilidad con Excel en Windows."""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(columnas)
        for fila in filas:
            writer.writerow(fila)

        # Retornar como bytes con BOM utf-8-sig
        return output.getvalue().encode('utf-8-sig')

    @staticmethod
    def exportar_a_pdf(
        titulo: str,
        columnas: List[str],
        filas: List[List[Any]],
        info_adicional: Optional[str] = None,
        horizontal: bool = False
    ) -> bytes:
        """Genera un documento PDF estilizado y profesional usando ReportLab."""
        buffer = io.BytesIO()
        pagesize = landscape(letter) if horizontal else letter
        doc = SimpleDocTemplate(
            buffer,
            pagesize=pagesize,
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        elements = []
        styles = getSampleStyleSheet()

        # Estilos personalizados
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#0d6efd'),
            alignment=1  # Centro
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#64748b'),
            alignment=1
        )
        cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10
        )
        cell_header_style = ParagraphStyle(
            'TableHeaderCell',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white
        )

        # Encabezado
        elements.append(Paragraph("SISTEMA DE GESTIÓN - MARROQUINERÍA ARTESANAL", subtitle_style))
        elements.append(Paragraph(titulo, title_style))
        fecha_gen = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Generado el: {fecha_gen}", subtitle_style))

        if info_adicional:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(info_adicional, subtitle_style))

        elements.append(Spacer(1, 14))

        # Preparar datos de la tabla con Paragraphs para ajuste automático de texto
        table_data = []

        # Fila de cabecera
        header_row = [Paragraph(f"<b>{col}</b>", cell_header_style) for col in columnas]
        table_data.append(header_row)

        # Filas de datos
        for r in filas:
            row_elements = []
            for item in r:
                text_val = str(item) if item is not None else "-"
                row_elements.append(Paragraph(text_val, cell_style))
            table_data.append(row_elements)

        # Tabla ReportLab
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))

        elements.append(t)
        doc.build(elements)
        return buffer.getvalue()

    # =========================================================================
    # 2. ADAPTADORES DE REPORTES (CONSULTA -> FORMATO PARA TABLA / CSV / PDF)
    # =========================================================================

    @staticmethod
    def obtener_datos_reporte(
        tipo: str,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ) -> Tuple[str, List[str], List[List[Any]], Optional[str]]:
        """Retorna (titulo, columnas, filas_datos, info_resumen) para el tipo de reporte solicitado."""
        
        info_fechas = ""
        if fecha_desde and fecha_hasta:
            info_fechas = f"Período: {fecha_desde} al {fecha_hasta}"
        elif fecha_desde:
            info_fechas = f"Desde: {fecha_desde}"
        elif fecha_hasta:
            info_fechas = f"Hasta: {fecha_hasta}"

        if tipo == "ventas_fechas":
            data = ReporteRepository.ventas_por_fecha(fecha_desde, fecha_hasta)
            titulo = "Reporte de Ventas por Período"
            columnas = ["Fecha", "Cant. Ventas", "Total Facturado ($)", "Ticket Promedio ($)"]
            filas = [
                [
                    r["dia"].strftime("%d/%m/%Y"),
                    r["cantidad_ventas"],
                    f"${r['total_facturado']:.2f}",
                    f"${r['ticket_promedio']:.2f}"
                ]
                for r in data["filas"]
            ]
            info = f"{info_fechas} | Total Facturado: ${data['total_facturado']:.2f} | Ventas: {data['total_ventas']} | Promedio: ${data['ticket_promedio_general']:.2f}".strip(" |")
            return titulo, columnas, filas, info

        elif tipo == "top_productos":
            data = ReporteRepository.top_productos_mas_vendidos(fecha_desde, fecha_hasta)
            titulo = "Top 10 Productos Más Vendidos"
            columnas = ["Puesto", "ID", "Producto", "Categoría", "Unidades Vendidas", "Total Recaudado ($)"]
            filas = [
                [
                    idx + 1,
                    r["id_producto"],
                    r["nombre_producto"],
                    r["nombre_categoria"],
                    r["unidades_vendidas"],
                    f"${r['total_recaudado']:.2f}"
                ]
                for idx, r in enumerate(data)
            ]
            return titulo, columnas, filas, info_fechas

        elif tipo == "medios_pago":
            data = ReporteRepository.ventas_por_medio_pago(fecha_desde, fecha_hasta)
            titulo = "Ventas por Medio de Pago"
            columnas = ["ID", "Medio de Pago", "Ajuste (%)", "Cant. Ventas", "Monto Total Facturado ($)"]
            filas = [
                [
                    r["id_medio_pago"],
                    r["nombre_medio"],
                    f"{r['porcentaje_descuento_recargo']}%",
                    r["cantidad_ventas"],
                    f"${r['monto_total']:.2f}"
                ]
                for r in data
            ]
            return titulo, columnas, filas, info_fechas

        elif tipo == "compras_proveedor":
            data = ReporteRepository.compras_por_proveedor(fecha_desde, fecha_hasta)
            titulo = "Compras por Proveedor"
            columnas = ["ID", "Razón Social", "CUIT", "Cant. Compras", "Unidades Compradas", "Monto Total ($)"]
            filas = [
                [
                    r["id_proveedor"],
                    r["razon_social"],
                    r["cuit"],
                    r["cantidad_compras"],
                    r["unidades_compradas"],
                    f"${r['monto_total']:.2f}"
                ]
                for r in data
            ]
            return titulo, columnas, filas, info_fechas

        elif tipo == "devoluciones_motivo":
            data = ReporteRepository.devoluciones_por_motivo(fecha_desde, fecha_hasta)
            titulo = "Devoluciones Agrupadas por Motivo"
            columnas = ["Motivo", "Cant. Devoluciones", "Unidades Totales", "Monto Diferencia Total ($)"]
            filas = [
                [
                    r["motivo"],
                    r["cantidad_devoluciones"],
                    r["unidades_totales"],
                    f"${r['total_diferencia']:.2f}"
                ]
                for r in data
            ]
            return titulo, columnas, filas, info_fechas

        elif tipo == "stock_valorizado":
            data = ReporteRepository.stock_valorizado()
            titulo = "Inventario y Stock Valorizado al Costo"
            columnas = ["ID Var.", "Producto", "Categoría", "Color", "Talle", "Stock Actual", "Costo Unit. ($)", "Valorización Total ($)"]
            filas = [
                [
                    r["id_variante"],
                    r["nombre_producto"],
                    r["nombre_categoria"],
                    r["nombre_color"],
                    r["nombre_tamano"],
                    r["stock_actual"],
                    f"${r['precio_costo']:.2f}",
                    f"${r['valor_total']:.2f}"
                ]
                for r in data["filas"]
            ]
            info = f"Total Unidades: {data['total_unidades']} u. | Capital Total Invertido: ${data['valor_total_general']:.2f}"
            return titulo, columnas, filas, info

        elif tipo == "stock_bajo":
            data = ReporteRepository.variantes_stock_bajo()
            titulo = "Variantes en Estado Crítico / Stock Bajo"
            columnas = ["ID Var.", "Producto", "Categoría", "Color", "Talle", "Stock Actual", "Stock Mínimo", "Déficit / Faltante"]
            filas = [
                [
                    r["id_variante"],
                    r["nombre_producto"],
                    r["nombre_categoria"],
                    r["nombre_color"],
                    r["nombre_tamano"],
                    r["stock_actual"],
                    r["stock_minimo"],
                    f"{r['faltante_minimo']} u."
                ]
                for r in data
            ]
            info = f"Total de variantes en estado crítico: {len(data)}"
            return titulo, columnas, filas, info

        else:
            raise ValueError(f"Tipo de reporte '{tipo}' no reconocido.")
