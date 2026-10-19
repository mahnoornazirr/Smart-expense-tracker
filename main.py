import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"

CATEGORIES = [
    "Food",
    "Transport",
    "Education",
    "Shopping",
    "Bills",
    "Other"
]


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "ID", "Date", "Category",
                    "Amount", "Description"
                ]
            )
            writer.writeheader()


def load_expenses():
    initialize_file()

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def add_expense():
    print("\n--- Add New Expense ---")

    print("Categories:", ", ".join(CATEGORIES))
    category = input("Enter category: ").strip().title()

    if category not in CATEGORIES:
        print("Invalid category!")
        return

    try:
        amount = float(input("Enter amount (PKR): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    description = input("Enter description: ").strip()

    expenses = load_expenses()

    if expenses:
        next_id = max(int(e["ID"]) for e in expenses) + 1
    else:
        next_id = 1

    expense = {
        "ID": next_id,
        "Date": str(date.today()),
        "Category": category,
        "Amount": f"{amount:.2f}",
        "Description": description
    }

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=expense.keys()
        )
        writer.writerow(expense)

    print("Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    for expense in expenses:
        print(
            f'ID: {expense["ID"]} | '
            f'Date: {expense["Date"]} | '
            f'Category: {expense["Category"]} | '
            f'Amount: PKR {float(expense["Amount"]):.2f} | '
            f'Description: {expense["Description"]}'
        )


def show_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses to summarize.")
        return

    total = 0
    category_totals = {}

    for expense in expenses:
        amount = float(expense["Amount"])
        category = expense["Category"]

        total += amount

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount

    print("\n--- Expense Summary ---")
    print(f"Total Expenses: PKR {total:.2f}")
    print(f"Number of Expenses: {len(expenses)}")

    print("\nCategory-wise Spending:")

    for category, amount in category_totals.items():
        print(f"{category}: PKR {amount:.2f}")


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses to delete.")
        return

    view_expenses()

    try:
        expense_id = int(input("\nEnter expense ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    updated_expenses = [
        expense for expense in expenses
        if int(expense["ID"]) != expense_id
    ]

    if len(updated_expenses) == len(expenses):
        print("Expense ID not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = [
            "ID", "Date", "Category",
            "Amount", "Description"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(updated_expenses)

    print("Expense deleted successfully!")


def main():
    initialize_file()

    while True:
        print("\n===== SMART EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Expense Summary")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("Thank you for using Smart Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()