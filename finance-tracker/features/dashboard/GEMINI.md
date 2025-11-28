# Day 7: Web Dashboard

## Today's Goal
Create a web-based dashboard using Streamlit to visualize financial data, providing a more intuitive and interactive user experience.

## Learning Focus
- Introduction to Streamlit
- Data visualization with charts and graphs
- Building interactive web interfaces with Python
- Running a web server from a CLI application

## Fintech Concepts
- **Financial Dashboard**: A visual representation of key financial metrics.
- **Interactive Data Exploration**: Allowing users to filter and drill down into their data.

## Features to Build

### 1. Dashboard Overview
- Display key metrics:
    - Current Balance
    - Total Income (this month)
    - Total Expenses (this month)
- Use Streamlit's `st.metric` for a clean presentation.

### 2. Spending Analysis
- Display a pie chart showing spending distribution by category.
- Use `altair` or Streamlit's native charting capabilities.

### 3. Income vs. Expenses
- Display a bar chart comparing total income and expenses for the last few months.
- This will help visualize cash flow trends.

### 4. Recent Transactions
- Show a table of the 10 most recent transactions.
- Use `st.dataframe` to display the data in a clean, sortable table.

### 5. Launch from Main Menu
- Add a "Launch Dashboard" option to `main.py`.
- This option will use `subprocess` or a similar module to run the Streamlit app.
