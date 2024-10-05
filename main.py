# Expense Tracker
import os
import json
import csv
import datetime
import argparse 

file_json = "expense.json"

def load_expense():
    if not os.path.exists(file_json):
        return []
    
    try:
        with open(file_json, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Warning: The JSON file is corrupted or invalid. Starting with an empty list.")
        return []


def save_expenses(expenses):
    with open(file_json, "w") as file:
        json.dump(expenses, file, indent=4)

def add(expenses, description, amount):
    new_id = len(expenses) + 1
    new_expense = {
        "id": new_id,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": description,
        "amount": float(amount),  # Ensure amount is float
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

def summary(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses: ${total:.2f}")

def summary_month(expenses, month):
    total = sum(expense["amount"] for expense in expenses if expense["date"].startswith(month))
    print(f"Total expenses for {month}: ${total:.2f}")

def delete(expenses, expense_id):
    found = False
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense deleted successfully")
            found = True
            break
    if not found:
        print(f"Expense with ID {expense_id} not found.")

def list_expenses(expenses):
    print(f"ID     | DESCRIPTION  | DATE                 | AMOUNT")
    for expense in expenses:
        print(f"{expense['id']: <7}| {expense['description']: <13}| {expense['date']: <20}| ${expense['amount']:.2f}")

def export_csv(expenses):
    with open('expenses.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'description', 'amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)
    print("Expenses exported to expenses.csv")

def main():
    expenses = load_expense()

    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    
    parser.add_argument('--add', nargs=2, metavar=('description', 'amount'),
                        help='Add a new expense with description and amount')

    parser.add_argument('--summary', action='store_true',
                        help='Show total expenses')


    parser.add_argument('--summary-month', metavar='month', 
                        help='Show total expenses for a specific month (format: YYYY-MM)')


    parser.add_argument('--delete', type=int, metavar='expense_id',
                        help='Delete an expense by ID')


    parser.add_argument('--list', action='store_true',
                        help='List all expenses')


    parser.add_argument('--export', action='store_true',
                        help='Export expenses to CSV')

    args = parser.parse_args()


    expenses = load_expense()

    if args.add:
        description, amount = args.add
        add(expenses, description, amount)
    elif args.summary:
        summary(expenses)
    elif args.summary_month:
        summary_month(expenses, args.summary_month)
    elif args.delete is not None:
        delete(expenses, args.delete)
    elif args.list:
        list_expenses(expenses)
    elif args.export:
        export_csv(expenses)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
