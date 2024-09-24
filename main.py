import pandas as pd # type: ignore
from pymongo import MongoClient
from analyze import analyze_data
from export import generate_pdf, export_to_excel

# MongoDB connection setup
def connect_to_mongodb():
    client = MongoClient('localhost', 27017)  # Modify the host and port if needed
    db = client['financial_data']  # Name of the database
    return db

# Unified main function
def main():
    # Connect to MongoDB
    db = connect_to_mongodb()

    # Define initial capital
    initial_capital = 10000.0  # Starting capital

    # Fetch the data from MongoDB
    transactions = pd.DataFrame(list(db['combined_data'].find({"Category": "transaction"})))
    sales = pd.DataFrame(list(db['combined_data'].find({"Category": "sales"})))

    # Analyze data fetched from MongoDB
    summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity = analyze_data(transactions, sales, initial_capital)

    # Generate report filenames based on the current date
    pdf_filename = f"daily_financial_report {pd.Timestamp.now().strftime('%d %B %Y')}.pdf"
    xsl_filename = f"daily_financial_report {pd.Timestamp.now().strftime('%d %B %Y')}.xlsx"

    # Generate the PDF report
    generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, pdf_filename)
    print(f"PDF report has been saved to {pdf_filename}")

    # Export to Excel
    export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, xsl_filename)
    print(f"Excel report has been saved to {xsl_filename}")

if __name__ == "__main__":
    main()