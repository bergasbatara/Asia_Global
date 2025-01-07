# def analyze_data(transactions, sales, initial_capital):
#     # # Print DataFrame info for debugging
#     # print("Transactions shape:", transactions.shape)
#     # print("Sales shape:", sales.shape)
#     # print("Transactions columns:", transactions.columns.tolist())
#     # print("Sales columns:", sales.columns.tolist())

#     # Initialize variables
#     total_purchase = 0.0
#     total_sales = 0.0
#     sales_summary = {}
#     transaction_summary = {}

#     try:
#         # Process transactions if data exists
#         if not transactions.empty and 'Category' in transactions.columns:
#             transaction_values = transactions[transactions['Category'] == 'transaction']
#             if not transaction_values.empty:
#                 total_purchase = float(sum(transaction_values['Price'].astype(float) * 
#                                         transaction_values['Quantity'].astype(float)))
                
#                 # Create transaction summary
#                 for _, row in transaction_values.iterrows():
#                     product_id = row['Product_id']
#                     transaction_amount = float(row['Price']) * float(row['Quantity'])
#                     if product_id in transaction_summary:
#                         transaction_summary[product_id] += transaction_amount
#                     else:
#                         transaction_summary[product_id] = transaction_amount

#         # Process sales if data exists
#         if not sales.empty and 'Category' in sales.columns:
#             sales_values = sales[sales['Category'] == 'sales']
#             if not sales_values.empty:
#                 total_sales = float(sum(sales_values['Price'].astype(float) * 
#                                       sales_values['Quantity'].astype(float)))
                
#                 # Create sales summary
#                 for _, row in sales_values.iterrows():
#                     product_id = row['Product_id']
#                     sales_amount = float(row['Price']) * float(row['Quantity'])
#                     if product_id in sales_summary:
#                         sales_summary[product_id] += sales_amount
#                     else:
#                         sales_summary[product_id] = sales_amount

#         # Calculate financial metrics
#         final_capital = initial_capital - total_purchase + total_sales
#         net_profit = total_sales - total_purchase
#         total_assets = final_capital
#         total_liabilities = 800000  # Fixed liabilities
#         total_equity = total_assets - total_liabilities

#         # Create summary dictionary
        # summary = {
        #     'sales': sales_summary if sales_summary else {'No Data': 0},
        #     'transactions': transaction_summary if transaction_summary else {'No Data': 0},
        #     'total_sales': total_sales,
        #     'total_purchase': total_purchase,
        #     'net_profit': net_profit,
        #     'final_capital': final_capital,
        #     'total_assets': total_assets,
        #     'total_liabilities': total_liabilities,
        #     'total_equity': total_equity
        # }

        # return summary, total_sales, total_purchase, net_profit, final_capital, total_assets, total_liabilities, total_equity

#     except Exception as e:
#         print(f"Error in analyze_data: {e}")
#         # Return default values in case of error
#         return ({
#             'sales': {'No Data': 0},
#             'transactions': {'No Data': 0},
#             'total_sales': 0,
#             'total_purchase': 0,
#             'net_profit': 0,
#             'final_capital': initial_capital,
#             'total_assets': initial_capital,
#             'total_liabilities': 800000,
#             'total_equity': initial_capital - 800000
#         }, 0, 0, 0, initial_capital, initial_capital, 800000, initial_capital - 800000)


def analyze_financial_data(transactions, sales, initial_capital, report_type):
    """Unified financial data analysis function that handles different report types"""
    
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
                
                for _, row in transaction_values.iterrows():
                    product_id = row['Product_id']
                    transaction_amount = float(row['Price']) * float(row['Quantity'])
                    transaction_summary[product_id] = transaction_summary.get(product_id, 0) + transaction_amount

        # Process sales if data exists
        if not sales.empty and 'Category' in sales.columns:
            sales_values = sales[sales['Category'] == 'sales']
            if not sales_values.empty:
                total_sales = float(sum(sales_values['Price'].astype(float) * 
                                      sales_values['Quantity'].astype(float)))
                
                for _, row in sales_values.iterrows():
                    product_id = row['Product_id']
                    sales_amount = float(row['Price']) * float(row['Quantity'])
                    sales_summary[product_id] = sales_summary.get(product_id, 0) + sales_amount

        # Calculate core financial metrics
        final_capital = initial_capital - total_purchase + total_sales
        net_profit = total_sales - total_purchase
        total_assets = final_capital
        total_liabilities = 800000  # Fixed liabilities
        total_equity = total_assets - total_liabilities
        
        # Generate report based on type
        if report_type == 1: # Balance sheet
            return {
                'current_assets': final_capital,
                'fixed_assets': total_assets - final_capital,
                'total_assets': total_assets,
                'current_liabilities': total_liabilities * 0.3,  # Assuming 30% are current
                'long_term_liabilities': total_liabilities * 0.7,  # Assuming 70% are long-term
                'total_liabilities': total_liabilities,
                'total_equity': total_equity,
                'total_liabilities_and_equity': total_liabilities + total_equity
            }
            
        elif report_type == 2: # P&L
            return {
                'revenue': total_sales,
                'cost_of_goods_sold': total_purchase,
                'gross_profit': total_sales - total_purchase,
                'operating_expenses': total_purchase * 0.2,  # Assuming 20% of purchases are operating expenses
                'operating_income': net_profit - (total_purchase * 0.2),
                'net_income': net_profit
            }
            
        elif report_type == 3: # Cash Flow
            return {
                'operating_activities': net_profit,
                'investing_activities': -total_purchase,
                'financing_activities': initial_capital,
                'net_cash_flow': final_capital - initial_capital,
                'beginning_cash': initial_capital,
                'ending_cash': final_capital
            }
            
        elif report_type == 4: # Equity
            return {
                'initial_equity': initial_capital - total_liabilities,
                'net_income': net_profit,
                'total_equity': total_equity,
                'retained_earnings': net_profit * 0.7,  # Assuming 70% of profit is retained
                'dividends': net_profit * 0.3  # Assuming 30% of profit is distributed
            }
            
        elif report_type == 5: # Financial Statement 
            return {
                'balance_sheet': {
                    'total_assets': total_assets,
                    'total_liabilities': total_liabilities,
                    'total_equity': total_equity
                },
                'income_statement': {
                    'total_revenue': total_sales,
                    'total_expenses': total_purchase,
                    'net_income': net_profit
                },
                'cash_flow': {
                    'net_cash_flow': final_capital - initial_capital,
                    'ending_cash': final_capital
                }
            }
            
        else:  # Default financial report
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
            # return {
            #     'sales': sales_summary if sales_summary else {'No Data': 0},
            #     'transactions': transaction_summary if transaction_summary else {'No Data': 0},
            #     'total_sales': total_sales,
            #     'total_purchase': total_purchase,
            #     'net_profit': net_profit,
            #     'final_capital': final_capital,
            #     'total_assets': total_assets,
            #     'total_liabilities': total_liabilities,
            #     'total_equity': total_equity
            # }

    except Exception as e:
        print(f"Error in analyze_financial_data: {e}")
        return {
            'error': str(e),
            'sales': {'No Data': 0},
            'transactions': {'No Data': 0},
            'total_sales': 0,
            'total_purchase': 0,
            'net_profit': 0,
            'final_capital': initial_capital,
            'total_assets': initial_capital,
            'total_liabilities': total_liabilities,
            'total_equity': initial_capital - total_liabilities
        }
