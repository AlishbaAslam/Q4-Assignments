from datetime import datetime, timedelta
import random
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from features.transactions.transactions import get_transactions
from features.budgets.budgets import get_budgets

# Create a console object
console = Console()

# Define the path to the goals file
GOALS_FILE = "database/goals.txt"

def get_goals():
    """Reads all goals from the goals file."""
    try:
        with open(GOALS_FILE, "r") as file:
            lines = file.readlines()
        
        goals = {}
        for line in lines:
            name, amount = line.strip().split(",")
            goals[name] = int(amount)
        return goals
    except FileNotFoundError:
        return {}

def save_goal(name, amount):
    """Saves a goal to the goals file."""
    goals = get_goals()
    goals[name] = amount
    with open(GOALS_FILE, "w") as file:
        for name, amount in goals.items():
            file.write(f"{name},{amount}\n")

def get_income_stability(transactions):
    """Analyzes income stability over the last few months."""
    income_by_month = {}
    three_months_ago = datetime.now() - timedelta(days=90)
    
    for t in transactions:
        if t["type"] == "Income":
            transaction_date = datetime.strptime(t["date"], "%Y-%m-%d")
            if transaction_date > three_months_ago:
                month = transaction_date.strftime("%Y-%m")
                income_by_month[month] = income_by_month.get(month, 0) + t["amount"]
                
    if len(income_by_month) < 2:
        return "Irregular" # Not enough data

    income_amounts = list(income_by_month.values())
    average_income = sum(income_amounts) / len(income_amounts)
    
    # Check for significant variations
    for amount in income_amounts:
        if abs(amount - average_income) / average_income > 0.3: # 30% variation
            return "Irregular"
            
    return "Stable"

def daily_financial_check():
    """Displays a daily financial check with spending, budget, alerts, and tips."""
    console.print("[bold blue]Generating your daily financial check...[/bold blue]")

    # Get data
    transactions = get_transactions()
    budgets = get_budgets()
    
    # Calculate today's spending
    today = datetime.now().date()
    today_spending = sum(
        t["amount"] for t in transactions 
        if t["type"] == "Expense" 
        and datetime.strptime(t["date"], "%Y-%m-%d").date() == today
    )

    # Calculate daily budget
    total_budget = sum(budgets.values())
    days_in_month = (today.replace(day=28) + timedelta(days=4)).day
    daily_budget = total_budget / days_in_month if total_budget > 0 else 0
    remaining_daily_budget = daily_budget - today_spending
    
    # Generate alerts
    alerts = []
    
    # Budget warnings
    current_month = today.strftime("%Y-%m")
    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
        if utilization > 80:
            alerts.append(f"⚠️ [bold yellow]Budget Warning:[/bold yellow] {category} category is at {utilization:.2f}% of its budget.")

    # Large transaction alerts
    total_income_this_month = sum(
        t["amount"] for t in transactions 
        if t["type"] == "Income" 
        and t["date"].startswith(current_month)
    )
    if total_income_this_month > 0:
        for t in transactions:
            if t["type"] == "Expense" and t["amount"] > (total_income_this_month * 0.2):
                alerts.append(f"💸 [bold red]Large Transaction:[/bold red] A transaction of {t['amount']/100:.2f} for {t['description']} was detected.")

    # Generate a quick tip
    tips = [
        "Create a budget for your top spending categories.",
        "Review your subscriptions for potential savings.",
        "Try a 'no-spend' weekend to boost your savings.",
        "Use a shopping list to avoid impulse purchases.",
        "Automate your savings by setting up recurring transfers.",
        "Cook at home more often to save on food expenses."
    ]
    quick_tip = random.choice(tips)

    # Build the output
    check_text = (
        f"Today's Spending: [bold red]{today_spending / 100:.2f}[/bold red]\n"
        f"Daily Budget: [bold green]{daily_budget / 100:.2f}[/bold green]\n"
        f"Remaining: [bold {'green' if remaining_daily_budget >= 0 else 'red'}]{remaining_daily_budget / 100:.2f}[/bold {'green' if remaining_daily_budget >= 0 else 'red'}]\n\n"
    )

    if alerts:
        check_text += "[bold]Alerts:[/bold]\n"
        for alert in alerts:
            check_text += f"• {alert}\n"
        check_text += "\n"
    
    check_text += f"💡 [bold]Quick Tip:[/bold] {quick_tip}"

    console.print(
        Panel(
            check_text,
            title=f"📊 Daily Financial Check ({today.strftime('%b %d, %Y')})",
            expand=False,
            border_style="blue"
        )
    )

def generate_smart_recommendations():
    """Generates and displays smart financial recommendations."""
    console.print("[bold blue]Analyzing your financial habits for recommendations...[/bold blue]")

    transactions = get_transactions()
    budgets = get_budgets()
    recommendations = []

    current_month = datetime.now().strftime("%Y-%m")
    
    # Recommendation: Overspending categories
    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        if spent_amount > budget_amount:
            recommendations.append(f"Consider reducing spending in the [bold]{category}[/bold] category. You are over budget by {(spent_amount - budget_amount)/100:.2f}.")

    # Recommendation: Savings rate
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income" and t["date"].startswith(current_month))
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense" and t["date"].startswith(current_month))
    
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
        if savings_rate < 20:
            recommendations.append("Your savings rate is below 20%. Try the 50/30/20 rule (50% needs, 30% wants, 20% savings).")
        else:
            recommendations.append("Great job on your savings rate! Keep it up or consider increasing your savings goal.")

    # Recommendation: Irregular income
    income_stability = get_income_stability(transactions)
    if income_stability == "Irregular":
        recommendations.append("Your income seems irregular. Consider building an emergency fund covering 3-6 months of expenses.")

    # Recommendation: Set budgets
    if not budgets:
        recommendations.append("You haven't set any budgets. Setting budgets can help you take control of your spending.")

    if not recommendations:
        recommendations.append("You are doing great! Keep up the good financial habits.")

    rec_text = ""
    for rec in recommendations:
        rec_text += f"• {rec}\n"

    console.print(
        Panel(
            rec_text,
            title="💡 Smart Recommendations",
            expand=False,
            border_style="green"
        )
    )

def show_spending_alerts():
    """Displays all active spending alerts."""
    console.print("[bold blue]Checking for spending alerts...[/bold blue]")
    
    transactions = get_transactions()
    budgets = get_budgets()
    alerts = []
    
    current_month = datetime.now().strftime("%Y-%m")
    
    # Budget warnings
    for category, budget_amount in budgets.items():
        spent_amount = sum(
            t["amount"] for t in transactions
            if t["type"] == "Expense" 
            and t["category"] == category
            and t["date"].startswith(current_month)
        )
        utilization = (spent_amount / budget_amount) * 100 if budget_amount > 0 else 0
        if utilization > 80:
            alerts.append(f"⚠️ [bold yellow]Budget Warning:[/bold yellow] {category} category is at {utilization:.2f}% of its budget.")

    # Large transaction alerts
    total_income_this_month = sum(
        t["amount"] for t in transactions 
        if t["type"] == "Income" 
        and t["date"].startswith(current_month)
    )
    if total_income_this_month > 0:
        for t in transactions:
            if t["type"] == "Expense" and t["amount"] > (total_income_this_month * 0.2):
                alerts.append(f"💸 [bold red]Large Transaction:[/bold red] A transaction of {t['amount']/100:.2f} for {t['description']} was detected.")
    
    # Top spending categories
    category_spending = {}
    for t in transactions:
        if t["type"] == "Expense" and t["date"].startswith(current_month):
            category_spending[t["category"]] = category_spending.get(t["category"], 0) + t["amount"]
    
    if category_spending:
        top_category = max(category_spending, key=category_spending.get)
        alerts.append(f"📈 [bold]Top Spending Category:[/bold] Your highest spending this month is in the [bold]{top_category}[/bold] category.")

    if not alerts:
        alerts.append("No special alerts at the moment. Keep up the good work!")

    alert_text = ""
    for alert in alerts:
        alert_text += f"• {alert}\n"
        
    console.print(
        Panel(
            alert_text,
            title="🚨 Active Spending Alerts",
            expand=False,
            border_style="red"
        )
    )

def manage_savings_and_goals():
    """Menu for managing savings and goals."""
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "View Savings Opportunities",
            "Set a New Savings Goal",
            "View Goals Progress",
            "Go Back"
        ]
    ).ask()

    if choice == "View Savings Opportunities":
        view_savings_opportunities()
    elif choice == "Set a New Savings Goal":
        set_new_goal()
    elif choice == "View Goals Progress":
        view_goals_progress()
    else:
        return

def view_savings_opportunities():
    """Analyzes spending and suggests savings opportunities."""
    console.print("[bold blue]Finding savings opportunities...[/bold blue]")
    transactions = get_transactions()
    
    current_month = datetime.now().strftime("%Y-%m")
    category_spending = {}
    for t in transactions:
        if t["type"] == "Expense" and t["date"].startswith(current_month):
            category_spending[t["category"]] = category_spending.get(t["category"], 0) + t["amount"]
            
    if not category_spending:
        console.print("[bold green]No spending this month to analyze.[/bold green]")
        return
        
    sorted_categories = sorted(category_spending.items(), key=lambda item: item[1], reverse=True)
    
    savings_text = "You could save money in these categories:\n\n"
    for category, amount in sorted_categories[:3]:
        potential_savings = amount * 0.1 # Suggest saving 10%
        savings_text += f"• [bold]{category}[/bold]: You spent {amount/100:.2f}. Try reducing it by 10% to save {potential_savings/100:.2f}.\n"

    console.print(
        Panel(
            savings_text,
            title="💰 Savings Opportunities",
            expand=False,
            border_style="yellow"
        )
    )

def set_new_goal():
    """Sets a new savings goal."""
    console.print("[bold blue]Setting a new savings goal...[/bold blue]")
    name = questionary.text("What is the name of your goal? (e.g., Vacation, Emergency Fund)").ask()
    
    try:
        amount_str = questionary.text("What is the target amount?").ask()
        amount = int(float(amount_str) * 100)
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return
        
    save_goal(name, amount)
    console.print("[bold green]Savings goal set successfully![/bold green]")
    
def view_goals_progress():
    """Displays progress towards savings goals."""
    goals = get_goals()
    transactions = get_transactions()
    
    if not goals:
        console.print("[bold yellow]No savings goals set. Set one to get started![/bold yellow]")
        return

    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    total_savings = total_income - total_expenses
    
    progress_text = ""
    for name, amount in goals.items():
        progress = (total_savings / amount) * 100 if amount > 0 else 0
        progress_bar = ProgressBar(total=100, completed=min(progress, 100), width=30)
        progress_text += f"[bold]{name}[/bold] ({total_savings/100:.2f} / {amount/100:.2f})\n{progress_bar} {progress:.2f}%\n\n"
        
    console.print(
        Panel(
            progress_text,
            title="🎯 Goals Progress",
            expand=False,
            border_style="magenta"
        )
    )

