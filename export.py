import pandas as pd #type: ignore
from fpdf import FPDF #type: ignore
from datetime import datetime
from openpyxl import Workbook #type: ignore
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font #type: ignore
from openpyxl.utils.dataframe import dataframe_to_rows #type: ignore

class CustomPDF(FPDF):
    def footer(self):
        # Set the position at 1.5 cm from the bottom
        self.set_y(-15)
        
        # Add the logo image (adjust the path and size as needed)
        # self.image('/path/to/your/logo.png', 10, self.get_y(), 10)  # Adjust coordinates and size as needed
        
        # Set font for the footer
        self.set_font('Arial', 'I', 8)
        
        # Add website and email
        self.cell(0, 10, 'www.agf.co.id  |  office@agf.co.id', ln=False, align='L')

        # Add the date (on the right side)
        self.set_x(-30)  # Position on the right
        self.cell(0, 10, datetime.now().strftime('%d %B %Y'), ln=False, align='R')

def generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, filename):
    pdf = CustomPDF()  # Use the custom PDF class with the footer
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, f"Tanggal Laporan: {pd.Timestamp.now().strftime('%d %B %Y')}", ln=True, align='C')
    pdf.ln(5)

    # Table headers
    pdf.set_fill_color(200, 220, 255)  # Light blue background for header
    column_widths = [90, 40, 60]  # Define column widths
    pdf.set_font('Arial', 'B', 12)
    headers = ['Komponen', 'Product ID', 'Jumlah']
    for header in headers:
        pdf.cell(column_widths[headers.index(header)], 10, header, border=1, ln=0, align='C', fill=True)
    pdf.ln()

    # Table rows
    pdf.set_font('Arial', '', 12)
    for index, row in summary.iterrows():
        pdf.cell(column_widths[0], 10, "Pendapatan Jasa", border=1, ln=0)
        pdf.cell(column_widths[1], 10, str(int(row['Product_ID'])), border=1, ln=0, align='C')
        pdf.cell(column_widths[2], 10, f"Rp {row['Total_Sales_Amount']:,.2f}", border=1, ln=0, align='R')
        pdf.ln()

    # Total line
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(column_widths[0] + column_widths[1], 10, "Total Pendapatan", border=1, ln=0)
    pdf.cell(column_widths[2], 10, f"Rp {total_sales:,.2f}", border=1, ln=0, align='R')
    pdf.ln(10)

    # Reduce font size for additional sections
    pdf.set_font('Arial', '', 10)
    pdf.cell(190, 10, f"Laba Rugi Harian: Rp {net_profit:,.2f}", border=1, ln=1, align='L')
    pdf.cell(190, 10, f"Total Arus Kas: Rp {net_profit:,.2f}", border=1, ln=1, align='L')
    pdf.cell(190, 10, f"Saldo Kas Harian: Rp {final_capital:,.2f}", border=1, ln=1, align='L')

    # Aktiva dan Kewajiban Harian
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, "Aktiva dan Kewajiban Harian:", ln=1, align='L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(95, 10, f"Total Aset: Rp {total_assets:,.2f}", border=1, ln=0, align='L')
    pdf.cell(95, 10, f"Total Utang: Rp {total_liabilities:,.2f}", border=1, ln=0, align='L')
    pdf.ln()
    pdf.cell(95, 10, f"Total Ekuitas: Rp {total_equity:,.2f}", border=1, ln=1, align='L')

    # Output the PDF to a file
    pdf.output(filename)

def export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, filename):
    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Financial Report"

    # Define styles
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    number_format = '#,##0.00'
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Add column headers
    columns = ["Komponen", "Product ID", "Jumlah"]
    ws.append(columns)
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
        cell.alignment = Alignment(horizontal="center")

    # Append rows from DataFrame
    for r in dataframe_to_rows(summary, index=False, header=False):
        ws.append([f"Jasa {r[0]}", r[0], r[1]])

    # Format all rows
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
        for cell in row:
            cell.number_format = number_format
            cell.border = border

    # Add Total row
    ws.append(["Total Pendapatan", "", total_sales])
    # Merge the "Total Pendapatan" cell with the adjacent empty cell
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

    # Save the workbook
    wb.save(filename)
    

