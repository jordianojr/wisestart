import pandas as pd

# Read engaged users
engaged_df = pd.read_csv('engaged_user.csv', dtype={'card_owner_id': str})
# Read transaction profits
profit_df = pd.read_csv('../q1/transaction_profit.csv')

# Merge on card_token to get only transactions for engaged users
merged = pd.merge(profit_df, engaged_df[['card_token', 'card_owner_id', 'card_produced_time', 'profile_address_country']], on='card_token', how='inner')

# Group by card_owner_id and sum profit_gbp
result = merged.groupby(['card_owner_id', 'profile_address_country'], as_index=False).agg({
    'profit_gbp': 'sum',
    'card_produced_time': 'first',  # card_produced_time is the same for each owner_id
    'profile_address_country': 'first'
})
result.rename(columns={'profit_gbp': 'total_profit_gbp'}, inplace=True)

# Calculate months_since_joining
result['card_produced_time'] = pd.to_datetime(result['card_produced_time'])
reference_date = pd.Timestamp('2018-04-30')  # April has 30 days, not 31
result['months_since_joining'] = ((reference_date.year - result['card_produced_time'].dt.year) * 12 +
                                  (reference_date.month - result['card_produced_time'].dt.month)) + 1
result['12_month_ltv'] = round(result['total_profit_gbp'] / result['months_since_joining'] * 12, 2)

# Group by country and filter countries with more than 10 users
country_group = result.groupby('profile_address_country').agg(
    user_count=('card_owner_id', 'count'),
    avg_12_month_ltv=('12_month_ltv', 'mean')
).reset_index()
country_group = country_group[country_group['user_count'] > 10].sort_values(by='avg_12_month_ltv', ascending=False)

# Count transaction types per country
transaction_counts = merged.groupby(['profile_address_country', 'transaction_type']).size().unstack(fill_value=0)
# Rename columns for clarity
transaction_counts = transaction_counts.rename(columns={
    'CASH_WITHDRAWAL': 'atm_count',
    'POS_PURCHASE': 'pos_count',
    'ECOM_PURCHASE': 'ecom_count'
})
# Ensure all columns exist
for col in ['atm_count', 'pos_count', 'ecom_count']:
    if col not in transaction_counts.columns:
        transaction_counts[col] = 0
transaction_counts = transaction_counts[['atm_count', 'pos_count', 'ecom_count']]

# Merge transaction counts into country_group
country_group = country_group.merge(transaction_counts, left_on='profile_address_country', right_index=True, how='left').fillna(0)

# Save to CSV
result.to_csv('engaged_user_total_profit.csv', index=False)
country_group.to_csv('country_12_month_ltv.csv', index=False)

print(f"Average 12 months lifetime value for per active user in card user base: {result['12_month_ltv'].sum() / 1007}")
print(f"Average 12 months lifetime value for per acquired user in current card user base: {result['12_month_ltv'].sum() / 2901}")
print("\n12-month LTV by country (countries with >10 users):")
print(country_group)