from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create a console object
console = Console()

TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt"

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
        
def display_pie_chart(category_spending, total_spending):
    """Displays an ASCII pie chart of spending by category."""
    console.print("\n[bold blue]Spending by Category (ASCII Pie Chart):[/bold blue]")
    chart_width = 20
    for category, amount in category_spending.items():
        percentage = (amount / total_spending)
        bar_length = int(percentage * chart_width)
        bar = "█" * bar_length
        console.print(f"{category:<12} {bar} {percentage:.1%}")

def spending_analysis():
    """Analyzes spending patterns."""
    console.print("[bold blue]Spending Analysis[/bold blue]")
    transactions = get_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    now = datetime.now()
    current_month_str = now.strftime("%Y-%m")
    
    # Category Breakdown
    category_spending = {}
    total_spending_current_month = 0
    
    for t in transactions:
        if t["type"] == "Expense" and t["date"].startswith(current_month_str):
            category = t["category"]
            amount = t["amount"]
            category_spending[category] = category_spending.get(category, 0) + amount
            total_spending_current_month += amount

    if total_spending_current_month == 0:
        console.print("[bold yellow]No expenses found for the current month.[/bold yellow]")
        
    else:
        table = Table(title=f"Spending Breakdown for {current_month_str}")
        table.add_column("Category", style="cyan")
        table.add_column("Amount", style="magenta")
        table.add_column("Percentage", style="green")

        sorted_categories = sorted(category_spending.items(), key=lambda item: item[1], reverse=True)

        for category, amount in sorted_categories:
            percentage = (amount / total_spending_current_month) * 100
            table.add_row(
                category,
                f"{amount / 100:.2f}",
                f"{percentage:.2f}%"
            )
        
        console.print(table)
        
        display_pie_chart(category_spending, total_spending_current_month)

        # Top 3 Spending Categories
        console.print("\n[bold blue]Top 3 Spending Categories[/bold blue]")
        for i, (category, amount) in enumerate(sorted_categories[:3]):
            console.print(f"{i+1}. {category}: {amount / 100:.2f}")
            
        # Average Daily Expense
        days_in_month = now.day
        average_daily_expense = total_spending_current_month / days_in_month
        console.print(f"\n[bold blue]Average Daily Expense:[/bold blue] {average_daily_expense / 100:.2f}")

    # Monthly Comparison
    last_month = now - relativedelta(months=1)
    last_month_str = last_month.strftime("%Y-%m")
    
    total_spending_last_month = 0
    for t in transactions:
        if t["type"] == "Expense" and t["date"].startswith(last_month_str):
            total_spending_last_month += t["amount"]
            
    console.print(f"\n[bold blue]Monthly Comparison:[/bold blue]")
    console.print(f"Total spending this month: {total_spending_current_month / 100:.2f}")
    console.print(f"Total spending last month: {total_spending_last_month / 100:.2f}")

    if total_spending_current_month > total_spending_last_month:
        diff = total_spending_current_month - total_spending_last_month
        console.print(f"Spending is [bold red]up[/bold red] by {diff / 100:.2f} compared to last month.")
    elif total_spending_current_month < total_spending_last_month:
        diff = total_spending_last_month - total_spending_current_month
        console.print(f"Spending is [bold green]down[/bold green] by {diff / 100:.2f} compared to last month.")
    else:
        console.print("Spending is the same as last month.")


def income_analysis():
    """Analyzes income patterns."""
    console.print("[bold blue]Income Analysis[/bold blue]")
    transactions = get_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    now = datetime.now()
    current_month_str = now.strftime("%Y-%m")

    # Income by source
    income_sources = {}
    total_income_current_month = 0

    for t in transactions:
        if t["type"] == "Income" and t["date"].startswith(current_month_str):
            source = t["category"]
            amount = t["amount"]
            income_sources[source] = income_sources.get(source, 0) + amount
            total_income_current_month += amount
    
    if total_income_current_month == 0:
        console.print("[bold yellow]No income found for the current month.[/bold yellow]")
    else:
        table = Table(title=f"Income by Source for {current_month_str}")
        table.add_column("Source", style="cyan")
        table.add_column("Amount", style="magenta")
        table.add_column("Percentage", style="green")

        sorted_sources = sorted(income_sources.items(), key=lambda item: item[1], reverse=True)

        for source, amount in sorted_sources:
            percentage = (amount / total_income_current_month) * 100
            table.add_row(
                source,
                f"{amount / 100:.2f}",
                f"{percentage:.2f}%"
            )
        
        console.print(table)


    # Monthly Comparison
    last_month = now - relativedelta(months=1)
    last_month_str = last_month.strftime("%Y-%m")
    
    total_income_last_month = 0
    for t in transactions:
        if t["type"] == "Income" and t["date"].startswith(last_month_str):
            total_income_last_month += t["amount"]
    
    console.print(f"\n[bold blue]Monthly Comparison:[/bold blue]")
    console.print(f"Total income this month: {total_income_current_month / 100:.2f}")
    console.print(f"Total income last month: {total_income_last_month / 100:.2f}")

    if total_income_current_month > total_income_last_month:
        diff = total_income_current_month - total_income_last_month
        console.print(f"Income is [bold green]up[/bold green] by {diff / 100:.2f} compared to last month.")
    elif total_income_current_month < total_income_last_month:
        diff = total_income_last_month - total_income_current_month
        console.print(f"Income is [bold red]down[/bold red] by {diff / 100:.2f} compared to last month.")
    else:
        console.print("Income is the same as last month.")

    # Income Stability
    console.print("\n[bold blue]Income Stability:[/bold blue]")
    console.print("Your income seems stable. (Placeholder)")


def savings_analysis():
    """Analyzes savings patterns."""
    console.print("[bold blue]Savings Analysis[/bold blue]")
    transactions = get_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    now = datetime.now()
    
    # Current Month Savings
    current_month_str = now.strftime("%Y-%m")
    total_income_current_month = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(current_month_str))
    total_spending_current_month = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(current_month_str))
    savings_current_month = total_income_current_month - total_spending_current_month
    savings_rate = (savings_current_month / total_income_current_month) * 100 if total_income_current_month > 0 else 0
    
    console.print(f"\n[bold blue]Current Month Savings ({current_month_str}):[/bold blue]")
    console.print(f"Total Income: {total_income_current_month / 100:.2f}")
    console.print(f"Total Expenses: {total_spending_current_month / 100:.2f}")
    console.print(f"Savings: {savings_current_month / 100:.2f}")
    console.print(f"Savings Rate: {savings_rate:.2f}%")
    
    # Savings Trend (last 3 months)
    console.print("\n[bold blue]Savings Trend (Last 3 Months):[/bold blue]")
    for i in range(3):
        month = now - relativedelta(months=i)
        month_str = month.strftime("%Y-%m")
        
        income = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(month_str))
        expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(month_str))
        savings = income - expenses
        
        console.print(f"{month_str}: {savings / 100:.2f}")

def financial_health_score():
    """Calculates and displays a financial health score."""
    console.print("[bold blue]Financial Health Score[/bold blue]")
    
    transactions = get_transactions()
    budgets = get_budgets()
    
    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return
        
    now = datetime.now()
    current_month_str = now.strftime("%Y-%m")
    
    # 1. Savings Rate Score (30 points)
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(current_month_str))
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(current_month_str))
    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
    
    savings_rate_score = 0
    if savings_rate >= 20:
        savings_rate_score = 30
    elif savings_rate >= 10:
        savings_rate_score = 20
    elif savings_rate > 0:
        savings_rate_score = 10
        
    # 2. Budget Adherence Score (25 points)
    budget_adherence_score = 0
    if budgets:
        total_budget = sum(budgets.values())
        if total_budget > 0 and total_expenses <= total_budget:
            budget_adherence_score = 25
        elif total_budget > 0 and total_expenses <= total_budget * 1.1:
            budget_adherence_score = 15

    # 3. Income vs Expenses Score (25 points)
    income_vs_expenses_score = 0
    if total_income > total_expenses:
        income_vs_expenses_score = 25
    elif total_income > 0:
        income_vs_expenses_score = 10

    # 4. Debt Management Score (20 points) - Placeholder
    debt_management_score = 20 # Assuming no debt for now
    
    total_score = savings_rate_score + budget_adherence_score + income_vs_expenses_score + debt_management_score
    
    score_text = (
        f"Overall Score: [bold green]{total_score}/100[/bold green]\n\n"
        f"Breakdown:\n"
        f"- Savings Rate: {savings_rate_score}/30\n"
        f"- Budget Adherence: {budget_adherence_score}/25\n"
        f"- Income vs Expenses: {income_vs_expenses_score}/25\n"
        f"- Debt Management: {debt_management_score}/20\n\n"
        f"[bold blue]Recommendations:[/bold blue]\n"
    )

    if savings_rate < 10:
        score_text += "- Try to increase your savings rate.\n"
    if budget_adherence_score < 25:
        score_text += "- Review your budget adherence.\n"
    if income_vs_expenses_score < 25:
        score_text += "- Try to increase your income or reduce expenses.\n"

    console.print(Panel(score_text, title="Financial Health Score"))


def generate_monthly_report():
    """Generates a comprehensive monthly report."""
    console.print("[bold blue]Generating Monthly Report...[/bold blue]")
    
    transactions = get_transactions()
    budgets = get_budgets()
    
    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return
        
    now = datetime.now()
    current_month_str = now.strftime("%Y-%m")
    
    # Data gathering
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(current_month_str))
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(current_month_str))
    savings = total_income - total_expenses
    
    last_month = now - relativedelta(months=1)
    last_month_str = last_month.strftime("%Y-%m")
    total_income_last_month = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(last_month_str))
    total_expenses_last_month = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(last_month_str))

    # Report sections
    report = f"[bold green]Monthly Financial Report for {current_month_str}[/bold green]\n\n"
    
    report += "[bold]Month Overview:[/bold]\n"
    report += f"- Total Income: {total_income / 100:.2f}\n"
    report += f"- Total Expenses: {total_expenses / 100:.2f}\n"
    report += f"- Savings: {savings / 100:.2f}\n\n"

    report += "[bold]Income Summary:[/bold]\n"
    report += f"- This month: {total_income / 100:.2f}\n"
    report += f"- Last month: {total_income_last_month / 100:.2f}\n\n"
    
    report += "[bold]Expense Summary:[/bold]\n"
    report += f"- This month: {total_expenses / 100:.2f}\n"
    report += f"- Last month: {total_expenses_last_month / 100:.2f}\n\n"
    
    if budgets:
        report += "[bold]Budget Performance:[/bold]\n"
        for category, budget_amount in budgets.items():
            spent = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["category"] == category and t["date"].startswith(current_month_str))
            report += f"- {category}: Spent {spent/100:.2f} of {budget_amount/100:.2f}\n"
        report += "\n"

    report += "[bold]Top Transactions (Current Month):[/bold]\n"
    top_transactions = sorted([t for t in transactions if t["date"].startswith(current_month_str)], key=lambda t: t["amount"], reverse=True)[:5]
    for t in top_transactions:
        report += f"- {t['date']}: {t['description']} ({t['category']}) - {t['amount']/100:.2f}\n"
    report += "\n"
    
    report += "[bold]Trends:[/bold]\n"
    if total_expenses > total_expenses_last_month:
        report += "- Spending is trending up.\n"
    else:
        report += "- Spending is trending down.\n"

    report += "\n[bold]Next Month Projections:[/bold]\n"
    report += "- Projected spending: (Not implemented)\n"

    console.print(Panel(report, title="Monthly Report"))



