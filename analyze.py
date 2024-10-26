def analyze_data(transactions, sales, initial_capital):
    # Filter transactions data where Category is "transaction"
    transaction_values = transactions[transactions['Category'] == 'transaction']
    total_purchase = float(sum(transaction_values['Price'].astype(float) * transaction_values['Quantity'].astype(float)))

    # Filter sales data where Category is "sales"
    sales_values = sales[sales['Category'] == 'sales']
    total_sales = float(sum(sales_values['Price'].astype(float) * sales_values['Quantity'].astype(float)))

    # Prepare the summary dictionary with sales amounts per Product_ID
    sales_summary = {}
    for _, row in sales_values.iterrows():
        product_id = row['Product_id']
        sales_amount = float(row['Price']) * float(row['Quantity'])
        sales_summary[product_id] = sales_amount

    # Prepare the summary dictionary with transaction amounts per Product_ID
    transaction_summary = {}
    for _, row in transaction_values.iterrows():
        product_id = row['Product_id']
        transaction_amount = float(row['Price']) * float(row['Quantity'])
        transaction_summary[product_id] = transaction_amount

    # Calculate financial metrics
    final_capital = initial_capital - total_purchase + total_sales
    net_profit = total_sales - total_purchase
    total_assets = final_capital
    total_liabilities = 800000 # Assuming no liabilities in this example
    total_equity = total_assets - total_liabilities
    
    # Summary dictionary
    summary = {
        'sales': sales_summary,
        'transactions': transaction_summary,
        'total_sales': total_sales,
        'total_purchase': total_purchase,
        'net_profit': net_profit,
        'final_capital': final_capital,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity
    }

    return summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity