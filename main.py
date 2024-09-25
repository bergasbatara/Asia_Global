import pandas as pd # type: ignore
from pymongo import MongoClient
from analyze import analyze_data
from export import generate_pdf, export_to_excel
from datetime import datetime, timedelta

# MongoDB connection setup
def connect_to_mongodb():
    client = MongoClient('localhost', 27017)  # Modify the host and port if needed
    db = client['financial_data']  # Name of the database
    return db

# Function to calculate the start and end of the current week (Monday to Sunday)
def get_week_range():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

# Function to add data to the MongoDB collection
def add_data_to_db(db, date, time, product_id, quantity, price, category):
    new_data = {
        "Date": date,
        "Time": time,
        "Product_ID": product_id,
        "Quantity": quantity,
        "Price": price,
        "Category": category
    }

    # Insert the new data into the 'combined_data' collection
    db['combined_data'].insert_one(new_data)
    print(f"Inserted data into MongoDB: {new_data}")

# Function to fetch data for the current week from MongoDB
def fetch_weekly_data(db, category):
    start_of_week, end_of_week = get_week_range()

    # Convert start and end dates to strings in the format YYYY-MM-DD for MongoDB query
    start_date_str = start_of_week.strftime('%Y-%m-%d')
    end_date_str = end_of_week.strftime('%Y-%m-%d')

    # Fetch data within the week for the given category
    data = pd.DataFrame(list(db['combined_data'].find({
        "Category": category,
        "Date": {"$gte": start_date_str, "$lte": end_date_str}
    })))

    # Ensure the necessary columns are present and drop any unnecessary ones (like '_id')
    if '_id' in data.columns:
        data = data.drop('_id', axis=1)

    return data


# Unified main function
def main():
    # Connect to MongoDB
    db = connect_to_mongodb()

    while True:
        # Ask if the user wants to add new data or exit
        action = input("Do you want to add data or type 'exit' to stop? (add/exit): ").lower()

        if action == 'exit':
            break

        # Add new data (example usage)
        date = input("Enter Date (YYYY-MM-DD): ")
        time = input("Enter Time (HH:MM:SS): ")
        product_id = int(input("Enter Product ID: "))
        quantity = float(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        category = input("Enter Category (transaction/sales): ").lower()

        # Add the data to MongoDB
        add_data_to_db(db, date, time, product_id, quantity, price, category)

    # Define initial capital
    initial_capital = 10000.0  # Starting capital

    # Fetch weekly data from MongoDB
    transactions = fetch_weekly_data(db, "transaction")
    sales = fetch_weekly_data(db, "sales")

    # Analyze data fetched from MongoDB
    summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity = analyze_data(transactions, sales, initial_capital)

    # Generate report filenames based on the current date (weekly report)
    pdf_filename = f"weekly_financial_report_{pd.Timestamp.now().strftime('%d_%B_%Y')}.pdf"
    xsl_filename = f"weekly_financial_report_{pd.Timestamp.now().strftime('%d_%B_%Y')}.xlsx"

    # Generate the PDF report
    generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, pdf_filename)
    print(f"PDF report has been saved to {pdf_filename}")

    # Export to Excel
    export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, xsl_filename)
    print(f"Excel report has been saved to {xsl_filename}")

if __name__ == "__main__":
    main()

# mongod --dbpath /Users/bergasanargya/Asia_Global/mongodb_data
# laporan mingguan, bulanan, tahunan
# show dbs, use financial_data, show collections, db.combined_data.find().pretty()