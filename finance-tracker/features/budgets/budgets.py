import questionary
from rich.console import Console
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.panel import Panel
from datetime import datetime

# Create a console object
console = Console()

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
    """Sets a budget for a category."""
    console.print("[bold blue]Setting a new budget...[/bold blue]")

    category = questionary.select(
        "Select a category:",
        choices=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
    ).ask()

    try:
        amount_str = questionary.text("Enter the monthly budget amount:").ask()
        amount = int(float(amount_str) * 100)  # Store amount in cents
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    save_budget(category, amount)
    console.print("[bold green]Budget set successfully![/bold green]")

def view_budgets():
    """Displays the budget vs actual spending."""
    budgets = get_budgets()
    transactions = get_transactions()

    if not budgets:
        console.print("[bold yellow]No budgets set. Please set a budget first.[/bold yellow]")
        return

    table = Table(title="Budget vs Spending")
    table.add_column("Category", style="cyan")
    table.add_column("Budget", style="magenta")
    table.add_column("Spent", style="yellow")
    table.add_column("Remaining", style="green")
    table.add_column("Utilization", style="blue")
    table.add_column("Status", style="bold")

    current_month = datetime.now().strftime("%Y-%m")

    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        
        remaining_amount = budget_amount - spent_amount
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0

        status = ""
        if utilization < 70:
            status = "[green]OK[/green]"
        elif 70 <= utilization <= 100:
            status = "[yellow]Warning[/yellow]"
        else:
            status = "[red]Over[/red]"

        progress_bar = ProgressBar(total=100, completed=utilization, width=20)

        table.add_row(
            category,
            f"{budget_amount / 100:.2f}",
            f"{spent_amount / 100:.2f}",
            f"{remaining_amount / 100:.2f}",
            progress_bar,
            status
        )

    console.print(table)

def budget_summary():
    """Displays a summary of all budgets."""
    budgets = get_budgets()
    transactions = get_transactions()

    if not budgets:
        console.print("[bold yellow]No budgets set. Please set a budget first.[/bold yellow]")
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

    summary_text = (
        f"Total Monthly Budget: [bold green]{total_budget / 100:.2f}[/bold green]\n"
        f"Total Spent: [bold red]{total_spent / 100:.2f}[/bold red]\n"
        f"Total Remaining: [bold green]{total_remaining / 100:.2f}[/bold green]\n"
        f"Overall Utilization: {overall_utilization:.2f}%\n\n"
    )

    if over_budget_categories:
        summary_text += "[bold red]Categories Over Budget:[/bold red]\n"
        for category in over_budget_categories:
            summary_text += f"- {category}\n"
        summary_text += "\n"

    summary_text += "[bold blue]Recommendations:[/bold blue]\n"
    summary_text += "- Review your spending in over-budget categories.\n"

    console.print(
        Panel(
            summary_text,
            title="Budget Summary",
            expand=False
        )
    )
