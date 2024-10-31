import boto3 #type:ignore
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd #type: ignore
from analyze import analyze_data
from export import generate_pdf, export_to_excel, generate_bilingual_pdf_report

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Use your AWS region Jakarta

# Sample_Data table name
table_name = 'Sample_Data' 
table = dynamodb.Table(table_name)

# Function to add data to DynamoDB
def add_data_to_db(table, date, time, product_id, quantity, price, category):
    # Generate a unique ID for the partition key
    item_id = str(uuid.uuid4())

    # Construct the item to be added
    new_data = {
        'id': item_id,  # Unique ID for each record (partition key)
        'Product_id': str(product_id),  # Product ID as the sort key
        'Date': date,
        'Time': time,
        'Quantity': Decimal(str(quantity)),  # Quantity as a Decimal
        'Price': Decimal(str(price)),  # Price as a Decimal
        'Category': category
    }

    # Put the item into the table
    try:
        table.put_item(Item=new_data)
        print(f"Inserted data into DynamoDB: {new_data}")
    except Exception as e:
        print(f"Error inserting data into DynamoDB: {e}")

# Function to fetch data for a specific week
def fetch_data_for_week(table, category, start_of_week):
    end_of_week = start_of_week + timedelta(days=6)
    start_date_str = start_of_week.strftime('%Y-%m-%d')
    end_date_str = end_of_week.strftime('%Y-%m-%d')

    # Query DynamoDB for data within the specified week and category
    response = table.scan(
        FilterExpression=Attr('Date').between(start_date_str, end_date_str) & Attr('Category').eq(category)
    )
    
    data = pd.DataFrame(response['Items'])
    return data

# Function to fetch data for the entire year
def fetch_data_for_year(table, category, year):
    all_data = pd.DataFrame()

    # Make sure the year is passed correctly as an integer
    start_of_year = datetime(year, 1, 1)

    # Loop through all 52 weeks of the year
    for week_num in range(52):
        start_of_week = datetime(year, 1, 1) + timedelta(weeks=week_num)
        weekly_data = fetch_data_for_week(table, category, start_of_week)
        all_data = pd.concat([all_data, weekly_data], ignore_index=True)

    return all_data

# Function to fetch data for a specific month
def fetch_data_for_month(table, category, start_of_month):
    # Calculate the end of the month
    if start_of_month.month == 12:
        end_of_month = datetime(start_of_month.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = datetime(start_of_month.year, start_of_month.month + 1, 1) - timedelta(days=1)
    
    start_date_str = start_of_month.strftime('%Y-%m-%d')
    end_date_str = end_of_month.strftime('%Y-%m-%d')

    # Query DynamoDB for data within the specified month and category
    response = table.scan(
        FilterExpression=Attr('Date').between(start_date_str, end_date_str) & Attr('Category').eq(category)
    )
    
    data = pd.DataFrame(response['Items'])
    return data

# Unified main function
def main():
    
    while True:
        # Ask if the user wants to add new data or exit
        action = input("Do you want to add data or type 'exit' to stop? (add/exit): ").lower()

        if action == 'exit':
            break

        # Add new data
        date = input("Enter Date (YYYY-MM-DD): ")
        time = input("Enter Time (HH:MM): ")
        product_id = int(input("Enter Product ID: "))
        quantity = float(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        category = input("Enter Category (transaction/sales): ").lower()

        # Add the data to DynamoDB
        add_data_to_db(table, date, time, product_id, quantity, price, category)

    # Choosing between 
    choice_weekly_yearly = input("Do you want weekly or yearly report (Weekly/Monthly/Yearly)? ").lower()

    language_input = input("What language? (E for English, I for Indonesian) ").lower()

    # Determine report date and type
    if choice_weekly_yearly == 'weekly':
        start_of_week_str = input("Enter the start date for the week to report on (YYYY-MM-DD): ")
        report_date = datetime.strptime(start_of_week_str, '%Y-%m-%d')
        report_type = 'weekly'
    elif choice_weekly_yearly == 'monthly':
        year = int(input("Enter the year for the report: "))
        month = int(input("Enter the month (1-12) for the report: "))
        report_date = datetime(year, month, 1)
        report_type = 'monthly'
    elif choice_weekly_yearly == 'yearly':
        year = int(input("Enter the year for the report: "))
        report_date = datetime(year, 1, 1)
        report_type = 'yearly'
    else:
        print("Invalid choice. Exiting.")
        return

    # Fetch data based on report type
    if report_type == 'weekly':
        transactions = fetch_data_for_week(table, "transaction", report_date)
        sales = fetch_data_for_week(table, "sales", report_date)
        pdf_filename = f"weekly_financial_report_{report_date.strftime('%Y-%m-%d')}.pdf"
        xsl_filename = f"weekly_financial_report_{report_date.strftime('%Y-%m-%d')}.xlsx"
    elif report_type == 'monthly':
        transactions = fetch_data_for_month(table, "transaction", report_date)
        sales = fetch_data_for_month(table, "sales", report_date)
        pdf_filename = f"monthly_financial_report_{report_date.strftime('%Y-%m')}.pdf"
        xsl_filename = f"monthly_financial_report_{report_date.strftime('%Y-%m')}.xlsx"
    elif report_type == 'yearly':
        transactions = fetch_data_for_year(table, "transaction", report_date.year)
        sales = fetch_data_for_year(table, "sales", report_date.year)
        pdf_filename = f"yearly_financial_report_{report_date.year}.pdf"
        xsl_filename = f"yearly_financial_report_{report_date.year}.xlsx"

    initial_capital = 10000.0

    summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity = analyze_data(transactions, sales, initial_capital)

    if language_input == "i":
        # Generate the PDF report
        generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, pdf_filename, language_input, report_date, report_type)
        print(f"PDF report has been saved to {pdf_filename}")
    else: 
        generate_bilingual_pdf_report(pdf_filename, summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, report_date)
        print(f"PDF report has been saved to {pdf_filename}")
        
    # Export to Excel
    export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, xsl_filename, language_input)
    print(f"Excel report has been saved to {xsl_filename}")


if __name__ == "__main__":
    main()