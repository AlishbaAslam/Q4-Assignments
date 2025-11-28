import questionary
from rich.console import Console
import subprocess

from features.transactions import transactions
from features.budgets import budgets
from features.analytics import analytics
from features.smart_assistant import smart_assistant
from features.data_management import data_management
from features.dashboard import dashboard

# Create a console object
console = Console()

def handle_transaction_management():
    """Handles the transaction management functionality."""
    while True:
        choice = questionary.select(
            "Transaction Management",
            choices=[
                "Add Expense",
                "Add Income",
                "List Transactions",
                "Show Balance",
                "Back"
            ]
        ).ask()

        if choice == "Add Expense":
            transactions.add_expense()
        elif choice == "Add Income":
            transactions.add_income()
        elif choice == "List Transactions":
            transactions.list_transactions()
        elif choice == "Show Balance":
            transactions.show_balance()
        elif choice == "Back":
            break

def handle_budget_management():
    """Handles the budget management functionality."""
    while True:
        choice = questionary.select(
            "Budget Management",
            choices=[
                "Set Budget",
                "View Budgets",
                "Budget Summary",
                "Back"
            ]
        ).ask()

        if choice == "Set Budget":
            budgets.set_budget()
        elif choice == "View Budgets":
            budgets.view_budgets()
        elif choice == "Budget Summary":
            budgets.budget_summary()
        elif choice == "Back":
            break

def handle_analytics():
    """Handles the analytics functionality."""
    while True:
        choice = questionary.select(
            "Analytics",
            choices=[
                "Spending Analysis",
                "Income Analysis",
                "Savings Analysis",
                "Financial Health Score",
                "Generate Monthly Report",
                "Back"
            ]
        ).ask()

        if choice == "Spending Analysis":
            analytics.spending_analysis()
        elif choice == "Income Analysis":
            analytics.income_analysis()
        elif choice == "Savings Analysis":
            analytics.savings_analysis()
        elif choice == "Financial Health Score":
            analytics.financial_health_score()
        elif choice == "Generate Monthly Report":
            analytics.generate_monthly_report()
        elif choice == "Back":
            break


def handle_smart_assistant():
    """Handles the smart assistant functionality."""
    while True:
        choice = questionary.select(
            "Smart Assistant",
            choices=[
                "Daily Financial Check",
                "Smart Recommendations",
                "Spending Alerts",
                "Savings & Goals",
                "Back"
            ]
        ).ask()

        if choice == "Daily Financial Check":
            smart_assistant.daily_financial_check()
        elif choice == "Smart Recommendations":
            smart_assistant.generate_smart_recommendations()
        elif choice == "Spending Alerts":
            smart_assistant.show_spending_alerts()
        elif choice == "Savings & Goals":
            smart_assistant.manage_savings_and_goals()
        elif choice == "Back":
            break

def handle_data_management():
    """Handles the data management functionality."""
    while True:
        choice = questionary.select(
            "Data Management",
            choices=[
                "Export to CSV",
                "Export to JSON",
                "Back"
            ]
        ).ask()

        if choice == "Export to CSV":
            data_management.export_to_csv()
        elif choice == "Export to JSON":
            data_management.export_to_json()
        elif choice == "Back":
            break

def handle_dashboard():
    """Launches the Streamlit web dashboard."""
    console.print("[bold yellow]Launching the web dashboard...[/bold yellow]")
    try:
        subprocess.run(["streamlit", "run", "features/dashboard/dashboard.py"])
    except FileNotFoundError:
        console.print("[bold red]Error: 'streamlit' command not found. Make sure Streamlit is installed.[/bold red]")


def main():
    """Main function to run the personal finance tracker."""

    console.print("[bold green]Welcome to your Personal Finance Tracker![/bold green]")

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Transaction management",
                "Budget management",
                "Analytics",
                "Smart Assistant",
                "Data Management",
                "Launch Dashboard",
                "Exit"
            ]
        ).ask()

        if choice == "Transaction management":
            handle_transaction_management()
        elif choice == "Budget management":
            handle_budget_management()
        elif choice == "Analytics":
            handle_analytics()
        elif choice == "Smart Assistant":
            handle_smart_assistant()
        elif choice == "Data Management":
            handle_data_management()
        elif choice == "Launch Dashboard":
            handle_dashboard()
        elif choice == "Exit":
            console.print("[bold red]Exiting the application. Goodbye![/bold red]")
            break

if __name__ == "__main__":
    main()
