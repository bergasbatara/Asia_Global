import pandas as pd #type: ignore

def analyze_data(transactions, sales, initial_capital=0.0):
    # Create explicit copies to avoid the SettingWithCopyWarning
    transactions = transactions.copy()
    sales = sales.copy()

    # Safely modify the DataFrame with .loc
    transactions['Total_Purchase_Amount'] = transactions['Quantity'] * transactions['Price']
    sales['Total_Sales_Amount'] = sales['Quantity'] * sales['Price']
    
    # Calculate overall capital change
    total_purchase = transactions['Total_Purchase_Amount'].sum()
    total_sales = sales['Total_Sales_Amount'].sum()
    final_capital = initial_capital - total_purchase + total_sales
    
    # Prepare summary for report
    summary = pd.merge(
        transactions.groupby('Product_ID')['Total_Purchase_Amount'].sum().reset_index(),
        sales.groupby('Product_ID')['Total_Sales_Amount'].sum().reset_index(),
        on='Product_ID', how='outer'
    )

    # Retaining the calculation for net profit, total assets, liabilities, and equity
    net_profit = total_sales - total_purchase
    total_assets = 40000000  # Example value (customize if needed)
    total_liabilities = 8000000  # Example value (customize if needed)
    total_equity = total_assets - total_liabilities

    return summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity
