import pandas as pd

# Load only necessary columns to save memory
card_df = pd.read_csv('../clean_data/card.csv', usecols=['card_token', 'card_owner_id', 'card_produced_time', 'profile_address_country', 'age_years'])
transaction_df = pd.read_csv('../clean_data/successful_transaction_clean.csv', usecols=['card_token', 'transaction_time'])

# Find unique card tokens used in successful transactions
used_card_tokens = set(transaction_df['card_token'].unique())

# Filter card_df for cards that were used
used_cards = card_df[card_df['card_token'].isin(used_card_tokens)]

# Count unique customers who used their card at least once
unique_customers = used_cards['card_owner_id'].nunique()
print(f"Number of customers who used their card at least once: {unique_customers}")

# Merge to get transaction times for used cards
merged = pd.merge(
    transaction_df,
    used_cards[['card_token', 'card_owner_id', 'card_produced_time', 'profile_address_country', 'age_years']],
    on='card_token',
    how='inner'
)

# Convert to datetime with error handling
merged['card_produced_time'] = pd.to_datetime(merged['card_produced_time'], errors='coerce')
merged['transaction_time'] = pd.to_datetime(merged['transaction_time'], errors='coerce')

# Find the first transaction for each card
first_txn = merged.groupby('card_token')['transaction_time'].min().reset_index()

# Merge back to get card_produced_time and card_owner_id
first_txn = pd.merge(
    first_txn,
    used_cards[['card_token', 'card_owner_id', 'card_produced_time', 'profile_address_country', 'age_years']],
    on='card_token',
    how='left'
)

# Convert again in case merge brought in strings
first_txn['card_produced_time'] = pd.to_datetime(first_txn['card_produced_time'], errors='coerce')
first_txn['transaction_time'] = pd.to_datetime(first_txn['transaction_time'], errors='coerce')

# Drop rows with missing dates
first_txn = first_txn.dropna(subset=['transaction_time', 'card_produced_time'])

# Check if first transaction is within one month of card production
first_txn['used_within_one_month'] = (first_txn['transaction_time'] - first_txn['card_produced_time']).dt.days <= 31
first_txn.drop('transaction_time', axis=1, inplace=True)

# Count unique customers who used their card within one month
customers_within_one_month = first_txn[first_txn['used_within_one_month']]['card_owner_id'].nunique()

print(f"Number of customers who used their card at least once within one month: {customers_within_one_month}")

first_txn.to_csv('engaged_user.csv', index=False)
