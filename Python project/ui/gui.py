import tkinter as tk
from tkinter import messagebox
from models.user import User
from database.db import create_tables, add_user, authenticate_user,update_expense_in_db,delete_expense_by_id

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.username = None
        self.user = None
        self.login_frame()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_frame(self):
        self.clear_window()
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if add_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.user = User(username, password)
            self.username = username
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Add Expense", command=self.expense_form).pack(pady=5)
        tk.Button(self.root, text="Total Expenses", command=self.show_total).pack(pady=5)
        tk.Button(self.root, text="Manage Expenses", command=self.view_expenses_screen).pack(pady=5)

    def expense_form(self):
        self.clear_window()
        tk.Label(self.root, text="Description").pack()
        desc_entry = tk.Entry(self.root)
        desc_entry.pack()
        tk.Label(self.root, text="Amount").pack()
        amt_entry = tk.Entry(self.root)
        amt_entry.pack()
        tk.Label(self.root, text="Date (YYYY-MM-DD)").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()
        tk.Label(self.root, text="Category").pack()
        cat_entry = tk.Entry(self.root)
        cat_entry.pack()

        def submit():
            try:
                desc = desc_entry.get()
                amt = float(amt_entry.get())
                date = date_entry.get()
                cat = cat_entry.get()
                self.user.add_expense(desc, amt, date, cat)
                messagebox.showinfo("Success", "Expense added.")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def show_total(self):
        total = self.user.get_total_expenses()
        messagebox.showinfo("Total Expenses", f"You've spent: ${total:.2f}")

    #

    def view_expenses_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Your Expenses", font=("Arial", 14)).pack(pady=10)

        for exp in self.user.get_expenses():
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)
            info = f"{exp.description} | ${exp.amount} | {exp.date} | {exp.category}"
            tk.Label(frame, text=info).pack(side="left")
            tk.Button(frame, text="Edit", command=lambda e=exp: self.edit_expense_screen(e)).pack(side="right")
            tk.Button(frame, text="Delete", command=lambda e=exp: self.delete_expense(e)).pack(side="right")

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def edit_expense_screen(self, expense):
        self.clear_window()
        tk.Label(self.root, text="Edit Expense", font=("Arial", 14)).pack(pady=10)

        desc = tk.Entry(self.root)
        desc.insert(0, expense.description)
        desc.pack()

        amt = tk.Entry(self.root)
        amt.insert(0, str(expense.amount))
        amt.pack()

        date = tk.Entry(self.root)
        date.insert(0, expense.date)
        date.pack()

        cat = tk.Entry(self.root)
        cat.insert(0, expense.category)
        cat.pack()

        def save():
            try:
                new_desc = desc.get()
                new_amt = float(amt.get())
                new_date = date.get()
                new_cat = cat.get()

                expense.edit_expense(new_desc, new_amt, new_date, new_cat)
                update_expense_in_db(expense)  
                messagebox.showinfo("Updated", "Expense updated.")
                self.main_menu()
                self.view_expenses_screen()
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(self.root, text="Save", command=save).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.view_expenses_screen).pack()

    def delete_expense(self, expense):
        delete_expense_by_id(expense.id)
        self.user.delete_expense_by_id(expense.id)
        messagebox.showinfo("Deleted", "Expense deleted.")
        self.view_expenses_screen()
        
        
    #

if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
