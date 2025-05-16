#GROUP 21
#NAME: CHIEMEZIE CHIDI ABDIEL  ID: 20232119
#NAME: VICTOR OLASEHINDE  ID: 20230660 
#NAME: ALIYU IBRAHIM ID: 20230018
import tkinter as tk  # Import tkinter for GUI components
from tkinter import messagebox  # Import messagebox to show popup alerts
from datetime import datetime  # Import datetime to handle dates on transactions
import json  # Import json module to save/load user data as files
import os  # Import os module to interact with file system like deleting files
import hashlib  # Import hashlib to securely hash passwords

# Class representing a single transaction like deposit or withdrawal
class Transaction:
    def __init__(self, t_type, amount, date=None):
        # Initialize transaction with type, amount, and optional date
        self.type = t_type
        self.amount = amount
        # If date given, parse it to datetime object; otherwise use current time
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if date else datetime.now()

    def __str__(self):
        # String representation of transaction with formatted date, type and amount
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} - {self.type}: ${self.amount:.2f}"

    def to_dict(self):
        # Convert transaction data to dictionary for JSON serialization
        return {
            "type": self.type,
            "amount": self.amount,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

# Class managing wallet operations like deposit, withdraw and storing transactions
class Wallet:
    def __init__(self):
        # Initialize wallet with zero balance and empty transaction list
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount):
        # Add amount to balance and record deposit transaction
        self.balance += amount
        self.transactions.append(Transaction("Deposit", amount))

    def withdraw(self, amount):
        # Check if balance is sufficient, then subtract and record withdrawal
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal")
        self.balance -= amount
        self.transactions.append(Transaction("Withdrawal", amount))

    def get_transaction_history(self):
        # Return list of transaction strings for display
        return [str(t) for t in self.transactions]

# Class to represent each user with username, hashed password and a wallet
class User:
    def __init__(self, username, password):
        # Initialize user with username, hashed password and a new wallet
        self.username = username
        self.password = password
        self.wallet = Wallet()

# Function to hash a plain text password using SHA-256
def hash_password(password):
    # Return the hashed hexadecimal string of the password
    return hashlib.sha256(password.encode()).hexdigest()

# Main application class handling all GUI and logic
class DigitalWalletApp:
    def __init__(self, master):
        # Save reference to root window and setup window properties
        self.master = master
        self.master.title("My Wallet")  # Window title
        self.master.geometry("550x500")  # Fixed window size
        self.master.configure(bg="#1F2739")  # Background color (dark blue/gray)
        self.user = None  # No user logged in initially
        self.login_screen()  # Show login screen first

    # Helper method to create styled label with customizable text, font, color
    def styled_label(self, text, font=("Helvetica", 18, "bold"), color="white"):
        return tk.Label(self.master, text=text, font=font, fg=color, bg=self.master["bg"])

    # Helper method to create styled entry box with optional password masking
    def styled_entry(self, show=None):
        # Larger font, padding, border style consistent across entries
        return tk.Entry(self.master, font=("Consolas", 18), bd=3, relief="groove", show=show, justify="center")

    # Helper method to create big styled buttons with consistent look
    def styled_button(self, text, command):
        # Big buttons with green background, white text, padding, and click command
        return tk.Button(
            self.master,
            text=text,
            font=("Verdana", 22, "bold"),
            bg="#00B894", fg="white",
            activebackground="#55EFC4",
            padx=60, pady=20,
            command=command
        )

    # Show login screen where user can enter username and password or register
    def login_screen(self):
        self.clear_window()  # Remove all widgets from window
        self.styled_label("Login or Register", font=("Impact", 26)).pack(pady=15)
        self.styled_label("Username:", font=("Helvetica", 18)).pack()
        self.username_entry = self.styled_entry()  # Username input field
        self.username_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_label("Password:", font=("Helvetica", 18)).pack()
        self.password_entry = self.styled_entry(show="*")  # Password input masked
        self.password_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_button("Login", self.login).pack(pady=12)
        self.styled_button("Register", self.register).pack(pady=12)

    # Show dashboard screen after login with balance and actions
    def dashboard(self):
        self.clear_window()
        self.styled_label(f"Welcome, {self.user.username}", font=("Georgia", 24), color="#FDCB6E").pack(pady=15)
        self.styled_label(f"Balance: ${self.user.wallet.balance:.2f}", font=("Courier", 24), color="#00CEC9").pack(pady=15)
        self.styled_button("Deposit", self.deposit_screen).pack(pady=12)
        self.styled_button("Withdraw", self.withdraw_screen).pack(pady=12)
        self.styled_button("Transaction History", self.show_history).pack(pady=12)
        self.styled_button("Logout", self.logout).pack(pady=12)
        self.styled_button("Delete Account", self.delete_account_screen).pack(pady=12)

    # Screen to enter deposit amount and confirm with password
    def deposit_screen(self):
        self.clear_window()
        self.styled_label("Enter deposit amount:", font=("Georgia", 22)).pack(pady=15)
        amount_entry = self.styled_entry()  # Entry for deposit amount
        amount_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_label("Enter password to confirm:", font=("Helvetica", 18)).pack()
        password_entry = self.styled_entry(show="*")  # Password confirmation
        password_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_button("Submit", lambda: self.make_deposit(amount_entry, password_entry)).pack(pady=15)
        self.styled_button("Back", self.dashboard).pack(pady=10)

    # Screen to enter withdrawal amount and confirm with password
    def withdraw_screen(self):
        self.clear_window()
        self.styled_label("Enter withdrawal amount:", font=("Georgia", 22)).pack(pady=15)
        amount_entry = self.styled_entry()  # Entry for withdrawal amount
        amount_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_label("Enter password to confirm:", font=("Helvetica", 18)).pack()
        password_entry = self.styled_entry(show="*")  # Password confirmation
        password_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_button("Submit", lambda: self.make_withdraw(amount_entry, password_entry)).pack(pady=15)
        self.styled_button("Back", self.dashboard).pack(pady=10)

    # Show list of past transactions in scrollable form if needed
    def show_history(self):
        self.clear_window()
        self.styled_label("Your Transaction History", font=("Arial Black", 22), color="#DFF9FB").pack(pady=15)
        history = self.user.wallet.get_transaction_history()  # Get list of transaction strings
        if not history:
            self.styled_label("No transactions yet.", font=("Arial", 16), color="#D63031").pack()
        else:
            # For each transaction, add a label showing details
            for t in history:
                tk.Label(self.master, text=t, font=("Arial", 14), fg="white", bg=self.master["bg"]).pack(pady=3)
        self.styled_button("Back", self.dashboard).pack(pady=15)

    # Screen to confirm account deletion with password prompt
    def delete_account_screen(self):
        self.clear_window()
        self.styled_label("Enter password to delete your account:", font=("Georgia", 22), color="red").pack(pady=15)
        password_entry = self.styled_entry(show="*")  # Password entry
        password_entry.pack(pady=10, ipady=8, ipadx=8)
        self.styled_button("Confirm Delete", lambda: self.delete_account(password_entry)).pack(pady=15)
        self.styled_button("Cancel", self.dashboard).pack(pady=10)

    # Perform account deletion if password matches
    def delete_account(self, password_entry):
        try:
            password = hash_password(password_entry.get())  # Hash entered password
            if password != self.user.password:
                raise ValueError("Incorrect password")  # Reject if wrong
            os.remove(f"{self.user.username}.json")  # Delete user data file
            messagebox.showinfo("Success", "Account deleted successfully")
            self.user = None
            self.login_screen()  # Go back to login screen
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Show error if something goes wrong

    # Deposit money after verifying password and amount validity
    def make_deposit(self, amount_entry, password_entry):
        try:
            amount = float(amount_entry.get())  # Convert input to float
            if amount <= 0:
                raise ValueError("Amount must be positive")  # Validate positive amount
            password = hash_password(password_entry.get())  # Hash entered password
            if password != self.user.password:
                raise ValueError("Incorrect password")  # Validate password
            self.user.wallet.deposit(amount)  # Perform deposit
            self.save_user_data()  # Save updated wallet to file
            messagebox.showinfo("Success", "Deposit successful")  # Confirm success
            self.dashboard()  # Return to dashboard
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error messages

    # Withdraw money after verifying password and sufficient balance
    def make_withdraw(self, amount_entry, password_entry):
        try:
            amount = float(amount_entry.get())  # Convert input to float
            if amount <= 0:
                raise ValueError("Amount must be positive")  # Validate positive amount
            password = hash_password(password_entry.get())  # Hash entered password
            if password != self.user.password:
                raise ValueError("Incorrect password")  # Validate password
            self.user.wallet.withdraw(amount)  # Perform withdrawal, may raise insufficient funds error
            self.save_user_data()  # Save updated wallet to file
            messagebox.showinfo("Success", "Withdrawal successful")  # Confirm success
            self.dashboard()  # Return to dashboard
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error messages

    # Login method verifies username and password, loads user data if exists
    def login(self):
        username = self.username_entry.get()  # Get entered username
        password = hash_password(self.password_entry.get())  # Hash entered password
        if os.path.exists(f"{username}.json"):  # Check if user file exists
            with open(f"{username}.json", "r") as f:
                data = json.load(f)  # Load user data from file
                if data["password"] == password:
                    # Create user object with wallet data
                    self.user = User(username, password)
                    self.user.wallet.balance = data["wallet"]["balance"]
                    # Load each transaction from saved data
                    for t_data in data["wallet"].get("transactions", []):
                        t = Transaction(t_data["type"], t_data["amount"], t_data["date"])
                        self.user.wallet.transactions.append(t)
                    self.dashboard()  # Show dashboard after successful login
                    return
        messagebox.showerror("Error", "Incorrect username or password")  # Show error if failed

    # Register new user if username not taken and save hashed password
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return
        if os.path.exists(f"{username}.json"):
            messagebox.showerror("Error", "Username already exists")
        else:
            hashed_password = hash_password(password)  # Hash password before saving
            self.user = User(username, hashed_password)  # Create user object
            self.save_user_data()  # Save new user data to file
            messagebox.showinfo("Success", "Account created successfully")
            self.dashboard()  # Go to dashboard

    # Save current user data to JSON file
    def save_user_data(self):
        data = {
            "password": self.user.password,  # Save hashed password
            "wallet": {
                "balance": self.user.wallet.balance,  # Save balance
                "transactions": [t.to_dict() for t in self.user.wallet.transactions]  # Save transaction list
            }
        }
        with open(f"{self.user.username}.json", "w") as f:
            json.dump(data, f)  # Write data to user's json file

    # Logout clears user and goes back to login screen
    def logout(self):
        self.user = None
        self.login_screen()

    # Remove all widgets from window to prepare for new screen
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Create main Tkinter window and start the app
root = tk.Tk()
app = DigitalWalletApp(root)
root.mainloop()
