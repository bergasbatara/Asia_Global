import pandas as pd #type: ignore
# from fpdf import FPDF #type: ignore
from reportlab.lib.pagesizes import A4 #type: ignore
from reportlab.lib import colors #type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle #type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer #type: ignore
from reportlab.pdfgen import canvas #type: ignore
from datetime import datetime
from openpyxl import Workbook #type: ignore
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font #type: ignore
from openpyxl.utils.dataframe import dataframe_to_rows #type: ignore

def generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, filename, language, report_date, report_type):
    # Setup for PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    
    # Custom styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', alignment=1, fontSize=16, spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TableHeader', alignment=1, fontSize=12, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Footer', fontSize=8, alignment=0))

    # Format header date based on report type
    if report_type == "yearly":
        header_text = f"Date of report for the year {report_date.year}" if language != 'i' else f"Tanggal Laporan untuk tahun {report_date.year}"
    elif report_type == "monthly":
        month_name = report_date.strftime('%B')
        header_text = f"Date of report for {month_name} {report_date.year}" if language != 'i' else f"Tanggal Laporan untuk {month_name} {report_date.year}"
    elif report_type == "weekly":
        start_of_week = report_date.strftime('%d %B %Y')
        end_of_week = (report_date + pd.Timedelta(days=6)).strftime('%d %B %Y')
        header_text = f"Date of report for the week of {start_of_week} to {end_of_week}" if language != 'i' else f"Tanggal Laporan untuk minggu {start_of_week} sampai {end_of_week}"
    else:
        header_text = "Date of report: " + report_date.strftime('%d %B %Y')  # Default to full date if type is unknown

    elements.append(Paragraph(header_text, styles['CenterTitle']))

    # Column names and titles based on language
    if language == 'i':
        column_names = ["Komponen", "Product ID", "Jumlah"]
        row_titles = ["Jasa Pendapatan", "Total Pendapatan", "Laba Rugi Harian", "Total Arus Kas", "Saldo Kas Harian", "Aktiva dan Kewajiban Harian", "Total Aset", "Total Utang", "Total Ekuitas"]
    else:
        column_names = ["Component", "Product ID", "Amount"]
        row_titles = ["Service Revenue", "Total Revenue", "Daily Profit and Loss", "Total Cash Flow", "Daily Cash Balance", "Daily Assets and Liabilities", "Total Assets", "Total Debt", "Total Equity"]

    # Table header row
    data = [column_names]
    
    # Add rows from summary
    for product_id, amount in summary.get('sales', {}).items():
        data.append([row_titles[0], product_id, f"Rp {amount:,.2f}"])
    
    # Add Total row
    data.append([row_titles[1], "", f"Rp {total_sales:,.2f}"])

    # Create the table and style it
    table = Table(data, colWidths=[150, 100, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Financial Summary section
    financial_data = [
        (row_titles[2], f"Rp {net_profit:,.2f}"),
        (row_titles[3], f"Rp {net_profit:,.2f}"),
        (row_titles[4], f"Rp {final_capital:,.2f}"),
        (row_titles[6], f"Rp {total_assets:,.2f}"),
        (row_titles[7], f"Rp {total_liabilities:,.2f}"),
        (row_titles[8], f"Rp {total_equity:,.2f}")
    ]

    # Add Financial Summary as a separate table
    summary_table_data = [[title, value] for title, value in financial_data]
    summary_table = Table(summary_table_data, colWidths=[250, 120])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(summary_table)

    # Footer setup
    def add_footer(canvas, doc):
        footer_left = "www.agf.co.id  |  office@agf.co.id"
        footer_right = f"Generated on: {datetime.now().strftime('%d %B %Y')}"

        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(10, 20, footer_left)  # Left-aligned footer text
        canvas.drawRightString(A4[0] - 10, 20, footer_right)  # Right-aligned footer text
        canvas.restoreState()

    # Build PDF with footer on each page
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)

def export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, filename, language):
    # Convert summary to a DataFrame if it's not already in the correct format
    summary_df = pd.DataFrame.from_dict(summary['sales'], orient='index', columns=['Total_Sales_Amount'])
    summary_df.reset_index(inplace=True)
    summary_df.rename(columns={'index': 'Product_ID'}, inplace=True)

    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Financial Report"

    # Define styles
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    number_format = '#,##0.00'
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    if language == 'i':
        # Add column headers
        columns = ["Komponen", "Product ID", "Jumlah"]
        ws.append(columns)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = Alignment(horizontal="center")

        # Append rows from DataFrame
        for r in dataframe_to_rows(summary_df, index=False, header=False):
            ws.append([f"Jasa {r[0]}", r[0], r[1]])

        # Format all rows
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
            for cell in row:
                cell.number_format = number_format
                cell.border = border

        # Add Total row
        ws.append(["Total Pendapatan", "", total_sales])
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=2)
        ws["C" + str(ws.max_row)].number_format = number_format
        ws["C" + str(ws.max_row)].border = border

        # Add Financial Summary
        financial_data = [
            ("Laba Rugi Harian", net_profit),
            ("Total Arus Kas", net_profit),
            ("Saldo Kas Harian", final_capital),
            ("Total Aset", total_assets),
            ("Total Utang", total_liabilities),
            ("Total Ekuitas", total_equity)
        ]

        for item in financial_data:
            ws.append(item)
            ws["B" + str(ws.max_row)].number_format = number_format
            ws["B" + str(ws.max_row)].border = border

        # Set column widths
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 20

    else:
        # Add column headers
        columns = ["Component", "Product ID", "Amount"]
        ws.append(columns)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = Alignment(horizontal="center")

        # Append rows from DataFrame
        for r in dataframe_to_rows(summary_df, index=False, header=False):
            ws.append([f"Service {r[0]}", r[0], r[1]])

        # Format all rows
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
            for cell in row:
                cell.number_format = number_format
                cell.border = border

        # Add Total row
        ws.append(["Total Sales", "", total_sales])
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=2)
        ws["C" + str(ws.max_row)].number_format = number_format
        ws["C" + str(ws.max_row)].border = border

        # Add Financial Summary
        financial_data = [
            ("Daily Profit and Loss", net_profit),
            ("Total Cash Flow", net_profit),
            ("Daily Cash Balance", final_capital),
            ("Total Assets", total_assets),
            ("Total Debt", total_liabilities),
            ("Total Equity", total_equity)
        ]

        for item in financial_data:
            ws.append(item)
            ws["B" + str(ws.max_row)].number_format = number_format
            ws["B" + str(ws.max_row)].border = border

        # Set column widths
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 20

    # Save the workbook
    wb.save(filename)

    

