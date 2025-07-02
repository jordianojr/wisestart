import pandas as pd

# Load card tokens from card.csv
card_df = pd.read_csv('card.csv')
card_tokens_set = set(card_df['card_token'])

# Load card tokens from successful_transaction_clean.csv
chunksize = 100000  # To handle large file
missing_tokens = set()
for chunk in pd.read_csv('successful_transaction_clean.csv', usecols=['card_token'], chunksize=chunksize):
    chunk_tokens = set(chunk['card_token'])
    missing = chunk_tokens - card_tokens_set
    missing_tokens.update(missing)

if missing_tokens:
    print(f"Missing card_tokens in card.csv: {len(missing_tokens)} found.")
    for token in list(missing_tokens)[:20]:  # Print up to 20 missing tokens
        print(token)
    if len(missing_tokens) > 20:
        print(f"...and {len(missing_tokens) - 20} more.")
else:
    print("All card_tokens in successful_transaction_clean.csv exist in card.csv.")
