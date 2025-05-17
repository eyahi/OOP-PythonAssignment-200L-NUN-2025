
from ui import cli
from database.db import create_tables,add_user,authenticate_user
from ui.gui import ExpenseTrackerGUI
import tkinter as tk
from models.user import User

def main():
    print("Welcome to the Expense Tracker")
    print("Choose interface:")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        create_tables()
        username = input("Username: ")
        password = input("Password: ")

        if authenticate_user(username, password):
            print("Login successful.")
            user = User(username, password)
            cli(user)
        else:
            print("Invalid credentials.")
    elif choice == "2":
        create_tables()
        root = tk.Tk()
        app = ExpenseTrackerGUI(root)
        root.mainloop()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

