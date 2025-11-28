from datetime import datetime, timedelta
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .data import get_transactions, save_transaction

# Create a console object
console = Console()

def add_expense():
    """Adds an expense transaction."""
    console.print("[bold blue]Adding a new expense...[/bold blue]")

    try:
        amount_str = questionary.text("Enter the amount:").ask()
        amount = int(float(amount_str) * 100)  # Store amount in cents
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    category = questionary.select(
        "Select a category:",
        choices=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
    ).ask()

    description = questionary.text("Enter a description:").ask()

    date_str = questionary.text("Enter the date (YYYY-MM-DD) or leave empty for today:").ask()
    if not date_str:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
            return

    save_transaction(date, "Expense", category, description, amount)
    console.print("[bold green]Expense added successfully![/bold green]")


def add_income():
    """Adds an income transaction."""
    console.print("[bold blue]Adding a new income...[/bold blue]")

    try:
        amount_str = questionary.text("Enter the amount:").ask()
        amount = int(float(amount_str) * 100)  # Store amount in cents
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    category = questionary.select(
        "Select a source:",
        choices=["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
    ).ask()

    description = questionary.text("Enter a description:").ask()

    date_str = questionary.text("Enter the date (YYYY-MM-DD) or leave empty for today:").ask()
    if not date_str:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
            return

    save_transaction(date, "Income", category, description, amount)
    console.print("[bold green]Income added successfully![/bold green]")

def list_transactions():
    """Lists all transactions."""
    transactions = get_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    filter_type = questionary.select(
        "Filter by:",
        choices=["All", "Expenses only", "Income only"]
    ).ask()

    filter_days = questionary.confirm("Filter by last 7 days?").ask()

    table = Table(title="Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="blue")
    table.add_column("Amount", justify="right", style="green")

    # Sort transactions by date (newest first)
    transactions.sort(key=lambda t: t["date"], reverse=True)
    
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d").date()
        
        # Filter by last 7 days
        if filter_days and transaction_date < seven_days_ago:
            continue
            
        amount_display = f"{transaction['amount'] / 100:.2f}"
        if transaction["type"] == "Expense":
            if filter_type == "Income only":
                continue
            table.add_row(
                transaction["date"],
                transaction["type"],
                transaction["category"],
                transaction["description"],
                f"[red]{amount_display}[/red]"
            )
        elif transaction["type"] == "Income":
            if filter_type == "Expenses only":
                continue
            table.add_row(
                transaction["date"],
                transaction["type"],
                transaction["category"],
                transaction["description"],
                f"[green]{amount_display}[/green]"
            )
    
    console.print(table)
    
def show_balance():
    """Calculates and displays the current balance."""
    transactions = get_transactions()
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = total_income - total_expenses

    balance_color = "green" if balance >= 0 else "red"

    balance_text = (
        f"Total Income: [green]{total_income / 100:.2f}[/green]\n"
        f"Total Expenses: [red]{total_expenses / 100:.2f}[/red]\n"
        f"Balance: [{balance_color}]{balance / 100:.2f}[/{balance_color}]"
    )
    
    console.print(
        Panel(
            balance_text,
            title="Current Balance",
            expand=False
        )
    )

