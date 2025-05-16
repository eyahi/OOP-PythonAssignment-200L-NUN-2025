import tkinter as tk
from tkinter import messagebox
import pyperclip
from password_manager import PasswordManager

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.pm = None
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Master Password:", font=("Arial", 12)).pack(pady=10)
        self.master_password_entry = tk.Entry(self.root, show="*")
        self.master_password_entry.pack()
        tk.Button(self.root, text="Login", command=self.authenticate).pack(pady=5)

    def authenticate(self):
        master_password = self.master_password_entry.get()
        if master_password:
            self.pm = PasswordManager(master_password)
            self.main_screen()
        else:
            messagebox.showerror("Error", "Master password required")

    def main_screen(self):
        self.clear_screen()

        header = tk.Label(self.root, text="Password Manager", bg="purple", fg="white", font=("Arial", 20, "bold"))
        header.pack(fill="x", pady=5)

        # Input Fields
        self.website_entry = self.create_labeled_entry("Website:")
        self.username_entry = self.create_labeled_entry("Username:")
        self.password_entry = self.create_labeled_entry("Password:", show="*")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save", bg="green", fg="white", width=12, command=self.save_entry).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Update", bg="blue", fg="white", width=12, command=self.update_entry).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", bg="red", fg="white", width=12, command=self.delete_entry).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(btn_frame, text="Copy Password", bg="pink", width=12, command=self.copy_password).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(btn_frame, text="Search", bg="yellow", width=12, command=self.search_entry).grid(row=1, column=1, columnspan=2, pady=5)

    def create_labeled_entry(self, label_text, show=None):
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = tk.Entry(frame, show=show)
        entry.pack(side=tk.LEFT, padx=5, pady=5)
        return entry

    def save_entry(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        self.pm.add_password(website, username, password)
        self.pm.save_to_file()
        messagebox.showinfo("Success", f"Password for '{website}' saved")

    def update_entry(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.pm.get_password(website):
            self.pm.update_password(website, username, password)
            self.pm.save_to_file()
            messagebox.showinfo("Updated", f"Password for '{website}' updated")
        else:
            messagebox.showerror("Error", "Website not found")

    def delete_entry(self):
        website = self.website_entry.get()
        if self.pm.get_password(website):
            self.pm.delete_password(website)
            self.pm.save_to_file()
            messagebox.showinfo("Deleted", f"Password for '{website}' deleted")
        else:
            messagebox.showerror("Error", "Website not found")

    def search_entry(self):
        website = self.website_entry.get()
        result = self.pm.get_password(website)
        if result:
            username, password = result
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
            messagebox.showinfo("Found", f"Credentials for '{website}' filled")
        else:
            messagebox.showerror("Error", "Website not found")

    def copy_password(self):
        website = self.website_entry.get()
        result = self.pm.get_password(website)
        if result:
            pyperclip.copy(result[1])
            messagebox.showinfo("Copied", f"Password for '{website}' copied to clipboard")
        else:
            messagebox.showerror("Error", "Website not found")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
