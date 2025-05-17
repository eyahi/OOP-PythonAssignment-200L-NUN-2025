from database.db import (
    create_tables, add_user, authenticate_user,
    add_expense_to_db, get_expenses, delete_expense_by_id,
    edit_category, delete_category
)
from models.user import User
from models.report import Report

def cli(user):
    while True:
        print("\n=== Expense Tracker CLI ===")
        print("1. View Expenses")
        print("2. Delete Expense by ID")
        print("3. Edit Category Name")
        print("4. Delete Category")
        print("5. Add Sample Expense")
        print("6. Show Report")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            expenses = get_expenses()
            for exp in expenses:
                print(exp)

        elif choice == "2":
            eid = input("Enter Expense ID to delete: ")
            delete_expense_by_id(eid)
            print("Expense deleted.")

        elif choice == "3":
            old = input("Old category name: ")
            new = input("New category name: ")
            edit_category(old, new)
            print("Category name updated.")

        elif choice == "4":
            cat = input("Category name to delete: ")
            delete_category(cat)
            print("Category deleted.")

        elif choice == "5":
            print("\nAdd a New Expense")
            description = input("Description: ")
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")

            user.add_expense(description, amount, date, category)
            print("Expense added successfully.")

       
        elif choice == "6":
            report = Report(user._User__username)  # Access private var
            report.generate_category_report()
            report.generate_pie_chart()

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

# Entry point when run from main.py
if __name__ == "__main__":
    create_tables()
    print("==== Expense Tracker CLI ====")
    username = input("Create a username: ")
    password = input("Create a password: ")

    if add_user(username, password):
        print("User registered successfully!")

    if authenticate_user(username, password):
        print("Login successful!")
        user = User(username, password)
        cli(user)
    else:
        print("Invalid login.")