"""""
# Runs user.py
from models.user import User

if __name__ == "__main__":
    # Initialize the database
    from database.db import initialize_database
    initialize_database()

    # Test user registration
    user = User(username="testuser", password="password123")
    user.save()

    # Test user authentication
    User.authenticate(username="testuser", password="password123")
    User.authenticate(username="testuser", password="wrongpassword")

# Runs expense.py
from models.expense import Expense

if __name__ == "__main__":
    # Initialize the database
    from database.db import initialize_database
    initialize_database()

    # Add a test expense
    expense = Expense(user_id=1, description="Lunch", amount=15.50, date="2025-05-11", category_id=1, vendor="TrayBlazerz")
    expense.save()

    # Retrieve and print all expenses for the user
    expenses = Expense.get_expenses_by_user(user_id=1)
    for exp in expenses:
        print(exp)

# Runs category.py
from models.category import Category

if __name__ == "__main__":
    # Initialize the database
    from database.db import initialize_database
    initialize_database()

    # Add a test category
    category = Category(name="Food")
    category.save()

    # Retrieve and print all categories
    categories = Category.get_all_categories()
    for cat in categories:
        print(cat)

# Runs report.py
from models.report import Report

if __name__ == "__main__":
    # Initialize the database
    from database.db import initialize_database
    initialize_database()

    pass  # Placeholder to ensure no action is taken at launch

"""""

# Now for the Main.py
import tkinter as tk
from tkinter import PhotoImage, messagebox, simpledialog
from models.user import User
from models.expense import Expense
from models.category import Category
from models.report import Report
from database.db import initialize_database, get_connection

class KoboKoApp:
    def __init__(self):
        # Initialize the database
        initialize_database()

        # Create the main application window
        self.root = tk.Tk()
        self.root.title("KoboKo")
        self.logged_in_user_id = None  # Track the logged-in user
        self.setup_welcome_page()

    # Other methods...

    def add_category(self):
        """Add a new category."""
        category_name = simpledialog.askstring("Add Category", "Enter category name:")
        if not category_name:
            return
        category = Category(name=category_name)
        category.save()
        messagebox.showinfo("Success", f"Category '{category_name}' added successfully!")   
        
    def setup_welcome_page(self):
        """Display the welcome page with logo, title, slogan, and buttons."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the window icon
        try:
            icon = PhotoImage(file="assets/icon.png")
            self.root.iconphoto(False, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")

        # Display the logo
        try:
            logo = PhotoImage(file="assets/logo.png")
            logo_label = tk.Label(self.root, image=logo)
            logo_label.image = logo  # Keep a reference to avoid garbage collection
            logo_label.grid(row=0, column=0, columnspan=2, pady=20)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Add welcome message and slogan
        welcome_label = tk.Label(self.root, text="Welcome to KoboKo!", font=("Arial", 16))
        welcome_label.grid(row=1, column=0, columnspan=2, pady=10)
        slogan_label = tk.Label(self.root, text="...if you no guide, you go cry", font=("Arial", 12), fg="gray")
        slogan_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Add Login and Register buttons only if the user is not logged in
        if self.logged_in_user_id is None:
            tk.Button(self.root, text="Register", command=self.register_user, width=20).grid(row=3, column=0, pady=5)
            tk.Button(self.root, text="Login", command=self.login_user, width=20).grid(row=3, column=1, pady=5)
        else:
            tk.Label(self.root, text="You are logged in!", font=("Arial", 12), fg="green").grid(row=3, column=0, columnspan=2, pady=10)

    def open_main_window(self, user_id):
        """Display the main window after login or registration."""
        # Save the logged-in user's ID
        self.logged_in_user_id = user_id

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Include the welcome page elements in every window
        self.setup_welcome_page()

        # Add buttons for expense and category management
        tk.Button(self.root, text="Add Expense", command=self.add_expense, width=20).grid(row=4, column=0, pady=5, padx=10)
        tk.Button(self.root, text="Add Category", command=self.add_category, width=20).grid(row=4, column=1, pady=5, padx=10)
        tk.Button(self.root, text="View Categories", command=self.view_categories, width=20).grid(row=5, column=0, pady=5, padx=10)
        tk.Button(self.root, text="View Expenses", command=self.view_expenses, width=20).grid(row=5, column=1, pady=5, padx=10)
        tk.Button(self.root, text="Generate Pie Chart", command=self.generate_pie_chart, width=20).grid(row=6, column=0, pady=5, padx=10)

        # Exit button
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, bg="red", fg="white").grid(row=6, column=1, pady=20, padx=10)

        # Add footer
        footer = tk.Label(self.root, text="BY:\n20232182 MrE\n20232100 David\n20232621 Mafe", 
                          font=("Arial", 9), fg="gray", anchor="e", justify="right")
        footer.grid(row=7, column=0, columnspan=2, pady=10)

    def register_user(self):
        """Handle user registration."""
        username = simpledialog.askstring("Register User", "Enter username:")
        if not username:
            return
        password = simpledialog.askstring("Register User", "Enter password:", show="*")
        if not password:
            return
        user = User(username=username, password=password)
        user.save()
        messagebox.showinfo("Success", f"User '{username}' registered successfully!")

    def login_user(self):
        """Handle user login."""
        username = simpledialog.askstring("Login", "Enter username:")
        if not username:
            return
        password = simpledialog.askstring("Login", "Enter password:", show="*")
        if not password:
            return
        if User.authenticate(username=username, password=password):
            # Fetch the logged-in user's ID
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]
            conn.close()

            messagebox.showinfo("Success", "Login successful!")
            self.open_main_window(user_id=user_id)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def add_expense(self):
        """Add a new expense for the logged-in user."""
        try:
            description = simpledialog.askstring("Add Expense", "Enter expense description:")
            if not description:
                return
            amount = float(simpledialog.askstring("Add Expense", "Enter expense amount (₦):"))
            date = simpledialog.askstring("Add Expense", "Enter date (YYYY-MM-DD):")
            if not date:
                return
            category_id = int(simpledialog.askstring("Add Expense", "Enter category ID:"))
            vendor = simpledialog.askstring("Add Expense", "Enter vendor:")
            if not vendor:
                return
            expense = Expense(user_id=self.logged_in_user_id, description=description, amount=amount, date=date, category_id=category_id, vendor=vendor)
            expense.save()
            messagebox.showinfo("Success", f"Expense of ₦{amount} added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def view_categories(self):
        """Display all categories and allow deletion."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        if not categories:
            messagebox.showinfo("Info", "No categories available.")
            return

        # Create a new window to display categories
        categories_window = tk.Toplevel(self.root)
        categories_window.title("View Categories")

        tk.Label(categories_window, text="Categories", font=("Arial", 14)).pack(pady=10)

        for category in categories:
            frame = tk.Frame(categories_window)
            frame.pack(anchor="w", padx=20, pady=5)

            tk.Label(frame, text=f"{category[0]}. {category[1]}", font=("Arial", 10)).pack(side="left")

            # Add a "Delete" button for each category
            delete_button = tk.Button(frame, text="Delete", command=lambda cat_id=category[0]: self.delete_category(cat_id))
            delete_button.pack(side="right")

    def delete_category(self, category_id):
        """Delete a category by its ID."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Category with ID {category_id} deleted successfully!")
        self.view_categories()  # Refresh the categories window

    def view_expenses(self):
        """Display all expenses in a table-like format (unsorted) and allow deletion."""
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch expenses and total amount
        cursor.execute("""
        SELECT e.id, e.description, e.amount, e.date, c.name AS category, e.vendor
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ?
        """, (self.logged_in_user_id,))
        expenses = cursor.fetchall()

        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (self.logged_in_user_id,))
        total_amount = cursor.fetchone()[0] or 0
        conn.close()

        if not expenses:
            messagebox.showinfo("Info", "No expenses available.")
            return

        # Create a new window to display expenses
        expenses_window = tk.Toplevel(self.root)
        expenses_window.title("View Expenses")

        # Title label
        tk.Label(expenses_window, text="Expenses (Unsorted)", font=("Arial", 14)).grid(row=0, column=0, columnspan=7, pady=10)

        # Create a table-like format
        headers = ["ID", "Description", "Amount (₦)", "Date", "Category", "Vendor", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(expenses_window, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid").grid(row=1, column=col, padx=5, pady=5)

        for row, expense in enumerate(expenses, start=2):
            for col, value in enumerate(expense):
                tk.Label(expenses_window, text=value, borderwidth=1, relief="solid").grid(row=row, column=col, padx=5, pady=5)

            # Add a "Delete" button for each expense
            delete_button = tk.Button(expenses_window, text="Delete", command=lambda exp_id=expense[0]: self.delete_expense(exp_id))
            delete_button.grid(row=row, column=len(headers) - 1, padx=5, pady=5)

        # Display the total amount at the bottom
        tk.Label(expenses_window, text=f"Total Amount: ₦{total_amount}", font=("Arial", 12, "bold"), fg="blue").grid(row=len(expenses) + 2, column=0, columnspan=7, pady=10)

    def delete_expense(self, expense_id):
        """Delete an expense by its ID."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Expense with ID {expense_id} deleted successfully!")
        self.view_expenses()  # Refresh the expenses window

    def generate_pie_chart(self):
        """Generate and display the pie chart for the logged-in user."""
        if not Report.generate_pie_chart(user_id=self.logged_in_user_id):
            messagebox.showinfo("Info", "No data available to generate the pie chart.")

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = KoboKoApp()
    app.run()