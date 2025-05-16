import tkinter as tk
from tkinter import messagebox
import json
import random
import string
import secrets

# PASSWORD GENERATOR
def generate_password():
    length = 12
    categories = {
        "uppercase": string.ascii_uppercase,
        "lowercase": string.ascii_lowercase,
        "digits": string.digits,
        "punctuation": string.punctuation
    }

    password = [
        secrets.choice(categories["uppercase"]),
        secrets.choice(categories["lowercase"]),
        secrets.choice(categories["digits"]),
        secrets.choice(categories["punctuation"]),
    ]

    all_chars = ''.join(categories.values())
    password += [secrets.choice(all_chars) for _ in range(length - 4)]
    random.shuffle(password)

    final_password = ''.join(password)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)

# SAVE PASSWORD
def save_password():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showwarning("Error", "Please leave no empty fields!")
        return

    data = {
        email: {
            "password": password
        }
    }

    try:
        with open("data.json", "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = {}

    existing_data.update(data)

    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Password saved successfully!")

# SEARCH PASSWORD
def search_password():
    email = email_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            if email in data:
                password = data[email]["password"]
                messagebox.showinfo(email, f"Password: {password}")
            else:
                messagebox.showinfo("Not Found", f"No password found for {email}.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found.")

# SHOW ALL PASSWORDS
def show_password_list():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror("Error", "No data file found.")
        return

    list_window = tk.Toplevel(window)
    list_window.title("Saved Passwords")
    list_window.geometry("500x400")

    scrollbar = tk.Scrollbar(list_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area = tk.Text(list_window, wrap="word", yscrollcommand=scrollbar.set)
    text_area.pack(expand=True, fill="both")
    scrollbar.config(command=text_area.yview)

    for email, details in data.items():
        password = details.get("password", "N/A")
        text_area.insert(tk.END, f"Email: {email}\nPassword: {password}\n\n")

# UI SETUP
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
tk.Label(text="Email/Username:").grid(row=1, column=0)
tk.Label(text="Password:").grid(row=2, column=0)

# Entries
email_entry = tk.Entry(width=35)
email_entry.grid(row=1, column=1, columnspan=2)
email_entry.insert(0, "email@example.com")

password_entry = tk.Entry(width=21)
password_entry.grid(row=2, column=1)

# Buttons
tk.Button(text="Generate Password", command=generate_password).grid(row=2, column=2)
tk.Button(text="Add", width=36, command=save_password).grid(row=3, column=1, columnspan=2)
tk.Button(text="Search", width=12, command=search_password).grid(row=1, column=2)
tk.Button(text="View All", width=36, command=show_password_list).grid(row=4, column=1, columnspan=2)

window.mainloop()
