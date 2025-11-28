import streamlit as st
import pandas as pd
from datetime import datetime

# Define the path to the budgets file
BUDGETS_FILE = "database/budgets.txt"
TRANSACTIONS_FILE = "database/transactions.txt"

def get_budgets():
    """Reads all budgets from the budgets file."""
    try:
        with open(BUDGETS_FILE, "r") as file:
            lines = file.readlines()
        
        budgets = {}
        for line in lines:
            category, amount = line.strip().split(",")
            budgets[category] = int(amount)
        return budgets
    except FileNotFoundError:
        return {}

def get_transactions():
    """Reads all transactions from the transactions file."""
    try:
        with open(TRANSACTIONS_FILE, "r") as file:
            lines = file.readlines()
        
        transactions = []
        for line in lines:
            date, transaction_type, category, description, amount = line.strip().split(",")
            transactions.append({
                "date": date,
                "type": transaction_type,
                "category": category,
                "description": description,
                "amount": int(amount)
            })
        return transactions
    except FileNotFoundError:
        return []

def save_budget(category, amount):
    """Saves a budget to the budgets file."""
    budgets = get_budgets()
    budgets[category] = amount
    with open(BUDGETS_FILE, "w") as file:
        for category, amount in budgets.items():
            file.write(f"{category},{amount}\n")


def set_budget():
    """Sets a budget for a category using Streamlit widgets."""
    st.subheader("🎯 Set a New Budget")

    category = st.selectbox(
        "Select a category:",
        ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
    )

    amount_str = st.number_input(
        "Enter the monthly budget amount:", 
        min_value=0.0, 
        step=0.01,
        format="%.2f"
    )

    if st.button("Set Budget"):
        if amount_str <= 0:
            st.error("❌ Amount must be a positive number.")
            return
        
        amount = int(amount_str * 100)  # Store amount in cents
        save_budget(category, amount)
        st.success(f"✅ Budget for {category} set to ${amount_str:.2f} successfully!")


def view_budgets():
    """Displays the budget vs actual spending."""
    budgets = get_budgets()
    transactions = get_transactions()

    if not budgets:
        st.warning("⚠️ No budgets set. Please set a budget first.")
        return

    st.subheader("📊 Budget vs Spending")

    current_month = datetime.now().strftime("%Y-%m")

    budget_data = []
    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        
        remaining_amount = budget_amount - spent_amount
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0

        if utilization < 70:
            status = "✅ OK"
        elif 70 <= utilization <= 100:
            status = "⚠️ Warning"
        else:
            status = "🔴 Over"

        budget_data.append({
            "Category": category,
            "Budget": f"${budget_amount / 100:.2f}",
            "Spent": f"${spent_amount / 100:.2f}",
            "Remaining": f"${remaining_amount / 100:.2f}",
            "Utilization (%)": f"{utilization:.1f}%",
            "Status": status
        })

    df = pd.DataFrame(budget_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Add progress bars for each category
    st.subheader("Budget Utilization")
    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{category}**")
            st.progress(min(utilization / 100, 1.0))
        with col2:
            st.write(f"{utilization:.1f}%")


def budget_summary():
    """Displays a summary of all budgets."""
    budgets = get_budgets()
    transactions = get_transactions()

    if not budgets:
        st.warning("⚠️ No budgets set. Please set a budget first.")
        return

    total_budget = sum(budgets.values())
    total_spent = 0
    over_budget_categories = []

    current_month = datetime.now().strftime("%Y-%m")

    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense"
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        total_spent += spent_amount
        if spent_amount > budget_amount:
            over_budget_categories.append(category)

    total_remaining = total_budget - total_spent
    overall_utilization = (total_spent / total_budget) * 100 if total_budget > 0 else 0

    st.subheader("💰 Budget Summary")
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Budget", f"${total_budget / 100:.2f}")
    with col2:
        st.metric("Total Spent", f"${total_spent / 100:.2f}")
    with col3:
        st.metric("Total Remaining", f"${total_remaining / 100:.2f}")
    with col4:
        st.metric("Utilization", f"{overall_utilization:.1f}%")

    # Over budget warning
    if over_budget_categories:
        st.error("🔴 **Categories Over Budget:**")
        for category in over_budget_categories:
            st.write(f"- {category}")

    # Recommendations
    st.info("""
    **💡 Recommendations:**
    - Review your spending in over-budget categories
    - Consider adjusting budgets for next month
    - Track daily expenses to stay within limits
    """)