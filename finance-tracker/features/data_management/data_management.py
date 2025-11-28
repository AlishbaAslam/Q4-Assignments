import csv
import json
from rich.console import Console
from features.transactions.transactions import get_transactions
from features.budgets.budgets import get_budgets
from features.smart_assistant.smart_assistant import get_goals

console = Console()

def export_to_csv():
    """Exports all transactions to a CSV file."""
    transactions = get_transactions()
    if not transactions:
        console.print("[yellow]No transactions to export.[/yellow]")
        return

    try:
        with open("transactions.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Date", "Type", "Category", "Description", "Amount"])
            # Write transaction data
            for t in transactions:
                writer.writerow([
                    t["date"],
                    t["type"],
                    t["category"],
                    t["description"],
                    t["amount"] / 100
                ])
        console.print("[green]Successfully exported transactions to transactions.csv[/green]")
    except IOError as e:
        console.print(f"[red]Error exporting to CSV: {e}[/red]")

def export_to_json():
    """Exports all financial data to a JSON file."""
    transactions = get_transactions()
    budgets = get_budgets()
    goals = get_goals()

    if not transactions and not budgets and not goals:
        console.print("[yellow]No data to export.[/yellow]")
        return

    data = {
        "transactions": transactions,
        "budgets": budgets,
        "goals": goals
    }

    try:
        with open("financial_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        console.print("[green]Successfully exported all data to financial_data.json[/green]")
    except IOError as e:
        console.print(f"[red]Error exporting to JSON: {e}[/red]")
