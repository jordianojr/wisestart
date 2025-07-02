# Wise Take Home Assessment

This repository contains a data analysis pipeline for card transaction and customer profitability. The project is organized into several folders, each with a specific role in the data processing and analysis workflow for different questions.

## Folder Structure

- **original_data/**: Contains the raw, unprocessed datasets, including transaction and cost structure data. These files are the starting point for all analysis.

- **clean_data/**: Contains scripts and outputs for cleaning and preprocessing the raw data. This includes cleaned versions of the card, transaction, cost structure, and currency rates data, as well as scripts for data validation.

- **q1/**: Contains scripts and outputs for calculating transaction-level and aggregated profit metrics. This includes profit calculations by transaction, transaction type, and region/cost type.

- **q2/**: Contains scripts and outputs for customer-level analysis, including customer engagement and 12-month lifetime value (LTV) calculations by country and user.

## Getting Started

1. Start with the scripts in `clean_data/` to generate cleaned datasets from the raw data in `original_data/`.
2. Use the scripts in `q1/` to calculate transaction-level and aggregated profit metrics.
3. Use the scripts in `q2/` to analyze customer engagement and compute LTV metrics.

For more details on each step and file, see the README.md in each subfolder. 