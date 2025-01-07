def analyze_data(transactions, sales, initial_capital):
    # # Print DataFrame info for debugging
    # print("Transactions shape:", transactions.shape)
    # print("Sales shape:", sales.shape)
    # print("Transactions columns:", transactions.columns.tolist())
    # print("Sales columns:", sales.columns.tolist())

    # Initialize variables
    total_purchase = 0.0
    total_sales = 0.0
    sales_summary = {}
    transaction_summary = {}

    try:
        # Process transactions if data exists
        if not transactions.empty and 'Category' in transactions.columns:
            transaction_values = transactions[transactions['Category'] == 'transaction']
            if not transaction_values.empty:
                total_purchase = float(sum(transaction_values['Price'].astype(float) * 
                                        transaction_values['Quantity'].astype(float)))
                
                # Create transaction summary
                for _, row in transaction_values.iterrows():
                    product_id = row['Product_id']
                    transaction_amount = float(row['Price']) * float(row['Quantity'])
                    if product_id in transaction_summary:
                        transaction_summary[product_id] += transaction_amount
                    else:
                        transaction_summary[product_id] = transaction_amount

        # Process sales if data exists
        if not sales.empty and 'Category' in sales.columns:
            sales_values = sales[sales['Category'] == 'sales']
            if not sales_values.empty:
                total_sales = float(sum(sales_values['Price'].astype(float) * 
                                      sales_values['Quantity'].astype(float)))
                
                # Create sales summary
                for _, row in sales_values.iterrows():
                    product_id = row['Product_id']
                    sales_amount = float(row['Price']) * float(row['Quantity'])
                    if product_id in sales_summary:
                        sales_summary[product_id] += sales_amount
                    else:
                        sales_summary[product_id] = sales_amount

        # Calculate financial metrics
        final_capital = initial_capital - total_purchase + total_sales
        net_profit = total_sales - total_purchase
        total_assets = final_capital
        total_liabilities = 800000  # Fixed liabilities
        total_equity = total_assets - total_liabilities

        # Create summary dictionary
        summary = {
            'sales': sales_summary if sales_summary else {'No Data': 0},
            'transactions': transaction_summary if transaction_summary else {'No Data': 0},
            'total_sales': total_sales,
            'total_purchase': total_purchase,
            'net_profit': net_profit,
            'final_capital': final_capital,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity
        }

        return summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity

    except Exception as e:
        print(f"Error in analyze_data: {e}")
        # Return default values in case of error
        return ({
            'sales': {'No Data': 0},
            'transactions': {'No Data': 0},
            'total_sales': 0,
            'total_purchase': 0,
            'net_profit': 0,
            'final_capital': initial_capital,
            'total_assets': initial_capital,
            'total_liabilities': 800000,
            'total_equity': initial_capital - 800000
        }, 0, 0, 0, initial_capital, initial_capital, 800000, initial_capital - 800000)
