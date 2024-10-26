import boto3
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
from analyze import analyze_data

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Use your AWS region

# Replace 'your_table_name' with your DynamoDB table name
table_name = 'Sample_Data'  # Replace with the correct table name
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

    if choice_weekly_yearly == 'weekly':
        start_of_week_str = input("Enter the start date for the week to report on (YYYY-MM-DD): ")
        start_of_week = datetime.strptime(start_of_week_str, '%Y-%m-%d')

        transactions = fetch_data_for_week(table, "transaction", start_of_week)
        sales = fetch_data_for_week(table, "sales", start_of_week)

        pdf_filename = f"weekly_financial_report_{start_of_week_str}_to_{(start_of_week + timedelta(days=6)).strftime('%Y-%m-%d')}.pdf"
        xsl_filename = f"weekly_financial_report_{start_of_week_str}_to_{(start_of_week + timedelta(days=6)).strftime('%Y-%m-%d')}.xlsx"

    elif choice_weekly_yearly == 'yearly':
        start_of_year = int(input("Enter the year for the report? "))
        transactions = fetch_data_for_year(table, "transaction", start_of_year)
        sales = fetch_data_for_year(table, "sales", start_of_year)

        # Generate report filenames based on the current date (weekly report)
        pdf_filename = f"yearly_financial_report_{start_of_year}.pdf"
        xsl_filename = f"yearly_financial_report_{start_of_year}.xlsx"

    initial_capital = 10000.0

    summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity = analyze_data(transactions, sales, initial_capital)

    # Generate the PDF report
    generate_pdf(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, pdf_filename, language_input)
    print(f"PDF report has been saved to {pdf_filename}")

    # Export to Excel
    export_to_excel(summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity, xsl_filename, language_input)
    print(f"Excel report has been saved to {xsl_filename}")

if __name__ == "__main__":
    main()