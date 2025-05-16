from tkinter import *
from password_manager import PasswordManager
from password_entry import PasswordEntry
from tkinter import messagebox
import random
import string

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("500x500")
        self.root.config(padx=40, pady=40, bg="#f7f7f7")  # Light background

        # Connect to backend logic
        self.manager = PasswordManager()

        #Logo Canvas 
        self.canvas = Canvas(self.root, height=150, width=150, bg="#f7f7f7", highlightthickness=0)
        try:
            self.logo_img = PhotoImage(file="logo.png")  # Load logo image
            self.canvas.create_image(75, 75, image=self.logo_img)
        except Exception as e:
            print("Logo not Loaded:", e)
        self.canvas.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        #Form Frame 
        self.form_frame = Frame(self.root, bg="#f7f7f7")
        self.form_frame.grid(row=1, column=0, columnspan=3)

        #Website Entry & Search
        Label(self.form_frame, text="Website:", font=("Arial", 11), bg="#f7f7f7").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.website_entry = Entry(self.form_frame, width=21, font=("Arial", 10))
        self.website_entry.grid(row=0, column=1, padx=5, pady=5)
        self.website_entry.focus()

        self.search_button = Button(self.form_frame, text="Search", width=12, command=self.search_password, bg="#FFC107", fg="black")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        #Email/Username 
        Label(self.form_frame, text="Email/Username:", font=("Arial", 11), bg="#f7f7f7").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = Entry(self.form_frame, width=35, font=("Arial", 10))
        self.email_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.email_entry.insert(0, "you@example.com")  # Default email

        # Password Entry & Generate
        Label(self.form_frame, text="Password:", font=("Arial", 11), bg="#f7f7f7").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = Entry(self.form_frame, width=21, font=("Arial", 10))
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.generate_button = Button(self.form_frame, text="Generate", width=12, command=self.generate_password, bg="#2196F3", fg="white")
        self.generate_button.grid(row=2, column=2, padx=5, pady=5)

        #Add Button 
        self.add_button = Button(self.root, text="Add Password", width=36, command=self.save, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.add_button.grid(row=3, column=0, columnspan=3, pady=20)

        #Delete button
        self.delete_button = Button(self.root, text="Delete Entry", width=36, command=self.delete_entry, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        self.delete_button.grid(row=4, column=0, columnspan=3, pady=5)

    # Generate Random Password
    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(12))  # 12-char password
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)

    #Save Password to File
    def save(self):
        website = self.website_entry.get().strip()
        username = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not username or not password:
            messagebox.showerror("Missing Info", "Please fill out all fields.")
            return

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Save this entry?\n\nEmail: {username}\nPassword: {password}"
        )

        if is_ok:
            entry = PasswordEntry(website, username, password)
            self.manager.add_password(entry)

            # Clear fields
            self.website_entry.delete(0, END)
            self.password_entry.delete(0, END)
            messagebox.showinfo("Saved", f"Password for {website} saved successfully.")

    # Search for Saved Password
    def search_password(self):
        website = self.website_entry.get().strip()

        if not website:
            messagebox.showwarning("Missing Info", "Please enter a website to search.")
            return

        entry = self.manager.get_password(website)

        if entry:
            # Autofill fields
            self.email_entry.delete(0, END)
            self.email_entry.insert(0, entry.username)

            self.password_entry.delete(0, END)
            self.password_entry.insert(0, entry.password)

            messagebox.showinfo(title=website, message="Details found and filled in!")
        else:
            messagebox.showerror("Not Found", f"No entry found for '{website}'.")

    # Delete Password Entry
    def delete_entry(self):
        website = self.website_entry.get().strip()
        if not website:
            messagebox.showwarning("Missing Info", "Please enter the website to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the entry for '{website}'?")
        if confirm:
            self.manager.delete_password(website)
            self.website_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)
            messagebox.showinfo("Deleted", f"Entry for '{website}' has been deleted.")

    # Master Password Prompt
def prompt_master_password():
        pw_window = Tk()
        pw_window.title("Master Password")
        pw_window.geometry("300x150")
        pw_window.eval('tk::PlaceWindow . center')
        pw_window.resizable(False, False)
    
        Label(pw_window, text="Enter Master Password", font=("Arial", 12)).pack(pady=10)
        pw_entry = Entry(pw_window, show="*", width=30)
        pw_entry.pack(pady=5)
        
        def check_password():
            if pw_entry.get() == "OOP-project":  
                pw_window.destroy()
            else:
                messagebox.showerror("Access Denied", "Incorrect Master Password.")
    
        Button(pw_window, text="Enter", command=check_password).pack(pady=10)
        pw_window.mainloop()

#Run the App
if __name__ == "__main__":
    prompt_master_password()
    root = Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

# Adding a view all button and method defeats the aim of the encryption and security of the password manager.
# The view all button would allow the user to see all passwords in plain text, which is not secure.
# The purpose of the password manager is to securely store and encrypt passwords, not to display them all at once.