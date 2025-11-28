# Day 6: Data Management

## Today's Goal
Provide users with the ability to export their financial data for backup or use in other applications.

## Learning Focus
- File I/O (CSV, JSON)
- Data serialization
- User-friendly data export options

## Fintech Concepts
- **Data Portability**: Allowing users to take their data with them.
- **Data Backup**: Ensuring users can save their data to prevent loss.

## Features to Build

### 1. Export to CSV
- Export all transactions to a `transactions.csv` file.
- Columns: `Date`, `Type`, `Category`, `Description`, `Amount`

### 2. Export to JSON
- Export all transactions, budgets, and goals to a single `financial_data.json` file.
- The JSON file will have a structured format, with keys for `transactions`, `budgets`, and `goals`.

### 3. Data Management Menu
- A new menu in `main.py` to access the export features.
- The menu should provide options for exporting to CSV or JSON.
