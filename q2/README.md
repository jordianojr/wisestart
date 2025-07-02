# Q2 Folder

This folder contains scripts and outputs for customer-level analysis, including customer engagement and 12-month lifetime value (LTV) calculations.

## Contents

- **calculate_customer_12ltv.py**: Script to calculate the 12-month LTV for engaged users, grouped by country and other metrics.
- **check_card_usage.py**: Script to identify engaged users (those who used their card at least once, and within one month of issuance).
- **country_12_month_ltv.csv**: Output file with average 12-month LTV by country, including transaction type counts.
- **engaged_user_total_profit.csv**: Output file with total profit and 12-month LTV for each engaged user.
- **engaged_user.csv**: List of engaged users, including card usage and demographic information.

## Usage

Run `check_card_usage.py` to generate the engaged user list. Then run `calculate_customer_12ltv.py` to compute LTV metrics and country-level summaries. 