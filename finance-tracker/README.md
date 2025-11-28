# 💰 Personal Finance Tracker CLI

A powerful command-line application for tracking expenses, managing budgets, and gaining financial insights. Built with Python, this fintech-inspired tool helps you take control of your personal finances.

## ✨ Features

### 📊 Transaction Management
- Track expenses and income with detailed categorization
- Add descriptions and dates to each transaction
- View transaction history with beautiful tables
- Filter transactions by time period
- Real-time balance calculation

### 💵 Budget Management
- Set monthly budgets for different categories
- Track spending against budgets
- Visual progress bars showing utilization
- Automatic alerts for overspending
- Budget resets monthly

### 📈 Financial Analytics
- Spending breakdown by category
- Income analysis and trends
- Savings rate calculation
- Financial health score (0-100)
- Monthly and comparative reports
- Burn rate tracking

### 🤖 Smart Assistant
- Daily financial check-ins
- Proactive spending alerts
- Personalized recommendations
- Savings opportunities identification
- Financial goal tracking

### 💾 Data Management
- Export to CSV and JSON
- Import transactions from CSV
- Automated backups
- Data integrity validation
- Monthly report generation

### 🌐 Web Dashboard
- Clean Streamlit-based interface
- Real-time balance overview
- Budget progress visualization
- Recent transactions display
- Mobile-friendly design

## 🚀 Quick Start

Navigate through the menu using arrow keys and Enter.

### Adding Transactions

**Add Expense:**
1. Select "Add Expense" from menu
2. Enter amount (e.g., 1250 for Rs 12.50)
3. Choose category (Food, Transport, Shopping, etc.)
4. Add description
5. Confirm date

**Add Income:**
1. Select "Add Income"
2. Enter amount
3. Choose source (Salary, Freelance, Business, etc.)
4. Add description
5. Confirm date

### Setting Budgets

1. Select "Set Budget"
2. Choose category
3. Enter monthly budget amount
4. View budget summary

### Viewing Analytics

- **Balance**: Shows total income, expenses, and current balance
- **Budget Status**: Displays utilization with progress bars
- **Monthly Report**: Comprehensive financial overview
- **Financial Health**: Score with recommendations

### Web Dashboard
Launch the web interface:
streamlit run dashboard.py

Access at `http://localhost:8501`

## 💡 Key Concepts

### Money Handling
All monetary values are stored as integers (paisa/cents) to avoid floating-point errors:

# Correct
amount_paisa = 1250      # Rs 12.50
display = amount / 100   # Display

# Wrong - Never use floats for money!
amount = 12.50

### Categories

**Expense Categories:**
- Food
- Transport
- Shopping
- Bills
- Entertainment
- Health
- Other

**Income Sources:**
- Salary
- Freelance
- Business
- Investment
- Gift
- Other

## 📊 Financial Health Score

Your financial health is calculated based on:
- **Savings Rate** (30 points): Percentage of income saved
- **Budget Adherence** (25 points): Staying within budgets
- **Income vs Expenses** (25 points): Positive cash flow
- **Debt Management** (20 points): Debt handling

Score interpretation:
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- Below 60: Needs Improvement

### Export Data

# From CLI menu
Select "Export Data" → Choose format (CSV/JSON)

### Import Transactions

# Prepare CSV with columns: date,type,category,description,amount
# Select "Import Transactions" from menu

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Questionary](https://github.com/tmbo/questionary) for interactive CLI
- [Streamlit](https://streamlit.io/) for web dashboard
- Inspired by modern fintech applications

## 📧 Support

**⭐ If you find this project helpful, please give it a star!**