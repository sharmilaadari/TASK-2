import json
from datetime import datetime

class Transaction:
    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'transaction_type': self.transaction_type,
            'date': self.date
        }

    @classmethod
    def from_dict(cls, data):
        transaction = cls(data['amount'], data['category'], data['transaction_type'])
        transaction.date = data['date']
        return transaction

class BudgetTracker:
    def __init__(self, filename='transactions.json'):
        self.filename = filename
        self.transactions = self.load_transactions()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return income - expenses

    def analyze_expenses(self):
        categories = {}
        for t in self.transactions:
            if t.transaction_type == 'expense':
                if t.category in categories:
                    categories[t.category] += t.amount
                else:
                    categories[t.category] = t.amount
        for category, total in categories.items():
            print(f"Category: {category}, Total Spent: {total}")

    def list_transactions(self):
        for idx, t in enumerate(self.transactions):
            print(f"{idx}. {t.transaction_type.capitalize()} of {t.amount} in {t.category} on {t.date}")

    def save_transactions(self):
        with open(self.filename, 'w') as f:
            transactions_dict = [t.to_dict() for t in self.transactions]
            json.dump(transactions_dict, f)

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as f:
                transactions_dict = json.load(f)
                return [Transaction.from_dict(t) for t in transactions_dict]
        except FileNotFoundError:
            return []

def main():
    budget_tracker = BudgetTracker()

    while True:
        print("\nBudget Tracker Application")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Budget")
        print("4. Analyze Expenses")
        print("5. List Transactions")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Income amount: "))
            category = input("Income category: ")
            transaction = Transaction(amount, category, 'income')
            budget_tracker.add_transaction(transaction)
        elif choice == '2':
            amount = float(input("Expense amount: "))
            category = input("Expense category: ")
            transaction = Transaction(amount, category, 'expense')
            budget_tracker.add_transaction(transaction)
        elif choice == '3':
            budget = budget_tracker.calculate_budget()
            print(f"Remaining budget: {budget}")
        elif choice == '4':
            budget_tracker.analyze_expenses()
        elif choice == '5':
            budget_tracker.list_transactions()
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
