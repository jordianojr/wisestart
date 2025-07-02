import pandas as pd

def calculate_revenue(row, rates_dict):
    """Calculate total revenue for a single transaction"""
        
    # Get cleaned amounts (now stored in original column names)
    amount_value = row['amount_value']
    amount_currency = row['amount_currency']
    billing_amount_value = row['billing_amount_value']
    billing_currency = row['billing_amount_currency']
    interchange_fee = row['inter_change_fee']
        
    # Convert amounts to GBP for comparison
    amount_gbp = amount_value * rates_dict.get(amount_currency, 1)
    billing_gbp = billing_amount_value * rates_dict.get(billing_currency, 1)
        
    # Convert interchange fee from billing currency to GBP
    interchange_fee_gbp = interchange_fee * rates_dict.get(billing_currency, 1)
        
    # Conversion revenue is the difference between billing and transaction amounts
    # plus any interchange fees (which can be negative) - now in GBP
    conversion_revenue = billing_gbp - amount_gbp
    total_revenue = billing_gbp - amount_gbp + interchange_fee_gbp
        
    return conversion_revenue, total_revenue

def calculate_cost(row, rates_dict, cost_structure):
    """Calculate total cost for a single transaction based on cost structure"""
        
    transaction_cost_type = row['transaction_cost_type']
    cost_region = row['cost_region']
    amount_value = row['amount_value']
    amount_currency = row['amount_currency']
        
    # Convert transaction amount to GBP
    amount_gbp = amount_value * rates_dict.get(amount_currency, 1)
        
    # Get applicable cost lines for this transaction type and region
    applicable_costs = cost_structure[
        (cost_structure['transaction_cost_type'] == transaction_cost_type) & 
        (cost_structure['cost_region'] == cost_region)
    ]
        
    total_cost = 0.0
    cost_breakdown = []
        
    for _, cost_line in applicable_costs.iterrows():
        cost_line_name = cost_line['cost_line']
        fixed_or_variable = cost_line['fixed_or_variable']
        cost_in_gbp = cost_line['cost_in_gbp']
        variable_fee = cost_line['variable_fee']
            
        # Calculate the cost amount
        if fixed_or_variable == 'Fixed':
            cost_amount = float(cost_in_gbp) if pd.notna(cost_in_gbp) else 0
        else:  # Variable
            if pd.notna(variable_fee):
                # Convert percentage to decimal
                fee_decimal = float(variable_fee)
                cost_amount = amount_gbp * fee_decimal
            else:
                cost_amount = 0
            
        total_cost += cost_amount
        cost_breakdown.append({
            'cost_line': cost_line_name,
            'cost_amount': cost_amount,
            'cost_type': fixed_or_variable
        })
        
    return total_cost

def calculate_profit(transactions, rates, cost_structure):
    
    # Convert currency rates to a dictionary for easy lookup
    rates_dict = rates.set_index('code')[['rate_compared_to_gbp']].to_dict()['rate_compared_to_gbp']
    
    # Apply the calculations to each transaction
    print(f"Calculating revenue for {len(transactions)} transactions")
    revenue_result = transactions.apply(calculate_revenue, axis=1, args=(rates_dict,))
    transactions['conversion_revenue_gbp'] = [r[0] for r in revenue_result]
    transactions['total_revenue_gbp'] = [r[1] for r in revenue_result]
    
    print(f"Calculating cost for {len(transactions)} transactions")
    cost_result = transactions.apply(calculate_cost, axis=1, args=(rates_dict, cost_structure))
    transactions['total_cost_gbp'] = cost_result
    
    # Calculate profit (revenue - costs)
    transactions['profit_gbp'] = transactions['total_revenue_gbp'] - transactions['total_cost_gbp']
    
    return transactions

def main():
    cost_structure_df = pd.read_csv('../clean_data/cost_structure_clean.csv')
    transaction_df = pd.read_csv('../clean_data/successful_transaction_clean.csv', low_memory=False)
    rates_df = pd.read_csv('../clean_data/rates.csv')

    transaction_with_profit_df = calculate_profit(transaction_df, rates_df, cost_structure_df)
    print(transaction_with_profit_df.head(10))
    print(f"Total revenue from {len(transaction_with_profit_df)} transactions: {transaction_with_profit_df['total_revenue_gbp'].sum()}")
    print(f"Total cost from {len(transaction_with_profit_df)} transactions: {transaction_with_profit_df['total_cost_gbp'].sum()}")
    print(f"Total profit from {len(transaction_with_profit_df)} transactions: {transaction_with_profit_df['profit_gbp'].sum()}")

    group_summary = transaction_with_profit_df.groupby('transaction_type')[['total_revenue_gbp', 'total_cost_gbp', 'profit_gbp']].sum()
    transaction_counts = transaction_with_profit_df['transaction_type'].value_counts().sort_index()
    group_summary['transaction_count'] = transaction_counts
    group_summary['average_profit'] = round(group_summary['profit_gbp'] / transaction_counts,2)
    print("\n=== Revenue, Cost, Profit, and Count by Transaction Type ===")
    print(group_summary)

    # Group by transaction_type, cost_region, and transaction_cost_type
    group_cols = ['transaction_type', 'cost_region', 'transaction_cost_type']
    detailed_group_summary = transaction_with_profit_df.groupby(group_cols)[['total_revenue_gbp', 'total_cost_gbp', 'profit_gbp']].sum()
    detailed_transaction_counts = transaction_with_profit_df.groupby(group_cols).size()
    detailed_group_summary['transaction_count'] = detailed_transaction_counts
    detailed_group_summary['average_profit'] = round(detailed_group_summary['profit_gbp'] / detailed_transaction_counts, 2)
    print("\n=== Revenue, Cost, Profit, and Count by Transaction Type, Cost Region, and Transaction Cost Type ===")
    print(detailed_group_summary)

    transaction_with_profit_df.to_csv('transaction_profit.csv', index=False)
    group_summary.to_csv('transaction_type_profit.csv')
    detailed_group_summary.to_csv('transaction_type_region_costtype_profit.csv')

if __name__ == "__main__":
    main() 