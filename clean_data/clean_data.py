import pandas as pd

def clean_amount(amount_str):
    """Clean amount string by removing commas and converting to float"""
    if pd.isna(amount_str) or amount_str == '':
        return 0.0
    return float(str(amount_str).replace(',', ''))

# clean cost_structure
cost_structure_df = pd.read_csv('../original_data/cost_structure.csv')
# Drop rows where cost_line is 'Interchange'
cost_structure_df['cost_in_gbp'] = pd.to_numeric(cost_structure_df['cost_in_gbp'].str.replace('£', ''), errors='coerce')
cost_structure_df['variable_fee'] = pd.to_numeric(cost_structure_df['variable_fee'].str.replace('%', ''), errors='coerce') / 100
cost_structure_df.fillna(0, inplace=True)

cost_structure_df.to_csv("cost_structure_clean.csv", index=False)

# clean transaction
transaction_df = pd.read_csv('../original_data/transaction.csv', low_memory=False)
successful_transaction_df = transaction_df[transaction_df['state'] == 'SUCCESS'].copy()

# replace original columns with cleaned versions
successful_transaction_df['amount_value'] = successful_transaction_df['amount_value'].apply(clean_amount)
successful_transaction_df['billing_amount_value'] = successful_transaction_df['billing_amount_value'].apply(clean_amount)
successful_transaction_df['inter_change_fee'] = successful_transaction_df['inter_change_fee'].apply(clean_amount)

print(successful_transaction_df['decline_reason'].sum())
successful_transaction_df = successful_transaction_df.drop(['decline_reason'], axis=1)

successful_transaction_df.to_csv("successful_transaction_clean.csv", index=False)
