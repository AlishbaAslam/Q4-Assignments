# features/transactions/data.py

TRANSACTIONS_FILE = "database/transactions.txt"

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

def save_transaction(date, transaction_type, category, description, amount):
    """Saves a transaction to the transactions file."""
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(f"{date},{transaction_type},{category},{description},{amount}\n")
