import altair
import streamlit as st
import pandas as pd
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from features.transactions.data import get_transactions
from features.budgets.budgets import get_budgets
from datetime import datetime

def run_dashboard():
    """Main function to run the Streamlit dashboard."""
    st.set_page_config(layout="wide")
    st.title("Personal Finance Dashboard")

    # Load data
    transactions = get_transactions()
    budgets = get_budgets()

    if not transactions:
        st.warning("No transactions found. Add some transactions to see your dashboard.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df["amount"] = df["amount"] / 100  # Convert paisa/cents to currency unit
    df["date"] = pd.to_datetime(df["date"])

    # --- Metrics ---
    st.header("This Month's Overview")
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_df = df[
        (df["date"].dt.month == current_month) & 
        (df["date"].dt.year == current_year)
    ]
    
    total_income = monthly_df[monthly_df["type"] == "Income"]["amount"].sum()
    total_expenses = monthly_df[monthly_df["type"] == "Expense"]["amount"].sum()
    current_balance = total_income - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    col3.metric("Current Balance", f"₹{current_balance:,.2f}")

    # --- Charts ---
    st.header("Spending Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        # Spending by category (Pie chart)
        expense_df = monthly_df[monthly_df["type"] == "Expense"]
        if not expense_df.empty:
            category_spending = expense_df.groupby("category")["amount"].sum()
            st.altair_chart(
                altair.Chart(category_spending.reset_index()).mark_arc().encode(
                    theta="amount",
                    color="category",
                    tooltip=["category", "amount"]
                ),
                use_container_width=True
            )
        else:
            st.info("No expenses this month to analyze.")
            
    with col2:
        # Income vs Expense (Bar chart)
        df["month_year"] = df["date"].dt.to_period("M").astype(str)
        monthly_summary = df.groupby(["month_year", "type"])["amount"].sum().unstack().fillna(0)
        st.bar_chart(monthly_summary)
        
    # --- Recent Transactions ---
    st.header("Recent Transactions")
    st.dataframe(df.sort_values("date", ascending=False).head(10))

if __name__ == "__main__":
    run_dashboard()
