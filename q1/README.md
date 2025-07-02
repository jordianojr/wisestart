# Q1 Folder

This folder contains scripts and outputs for calculating transaction-level and aggregated profit metrics.

## Contents

- **calculate_profit.py**: Main script to compute revenue, cost, and profit for each transaction, and to aggregate results by transaction type, region, and cost type.
- **transaction_profit.csv**: Output file with profit calculations for each transaction.
- **transaction_type_profit.csv**: Aggregated profit, revenue, and cost by transaction type.
- **transaction_type_region_costtype_profit.csv**: Aggregated profit, revenue, and cost by transaction type, region, and cost type.

## Usage

Run `calculate_profit.py` to generate all output CSVs. The script reads cleaned data from the `clean_data` folder and outputs results in this directory. 