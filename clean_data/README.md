# Clean Data Folder

This folder contains scripts and datasets used to clean and preprocess the original transaction and cost structure data for further analysis.

## Contents

- **card.csv**: Cleaned cardholder data, including card tokens, production time, owner ID, country, age, and delivery details.
- **cost_structure_clean.csv**: Cleaned cost structure data, with all monetary values and percentages standardized for analysis.
- **rates.csv**: Currency conversion rates to GBP and USD for all relevant currencies.
- **successful_transaction_clean.csv**: Cleaned transaction data, filtered to include only successful transactions and standardized amount fields.
- **check_transactions.py**: Script to verify that all card tokens in the transaction data exist in the cardholder data.
- **clean_data.py**: Main script for cleaning the original cost structure and transaction data, producing the cleaned CSVs above.

## Usage

Run `clean_data.py` to generate the cleaned datasets. Use `check_transactions.py` to validate the integrity of the card-token relationships between datasets. 