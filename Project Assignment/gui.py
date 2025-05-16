import tkinter as tk
from tkinter import messagebox
from diary import DiaryEntry, DiaryManager
from datetime import datetime

class DiaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("My Diary")
        self.master.geometry("900x500")
        self.master.configure(bg="#ffe6f0")
        self.manager = DiaryManager()

        self.setup_ui()

    def setup_ui(self):
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self.master, bg="#ffb6c1")
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)  # Ensure left panel stretches vertically

        self.right_frame = tk.Frame(self.master, bg="#fff0f5", padx=20, pady=20)
        self.right_frame.grid(row=0, column=1, sticky="nswe")

        self.bottom_frame = tk.Frame(self.master, bg="#ffe6f0")  # New bottom frame for date/time
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="we")
        self.master.grid_rowconfigure(1, weight=0)

        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_bottom_panel()  # Setup bottom panel

    def setup_left_panel(self):
        # Search bar
        self.search_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.search_entry.pack(fill="x", padx=10, pady=(5, 0))
        self.search_button = tk.Button(self.left_frame, text="Search", command=self.search_entries, bg="#5bc0de", fg="white")
        self.search_button.pack(pady=(0, 10))

        # Saved Entries label: Arial, size 12, bold
        tk.Label(
            self.left_frame,
            text="Saved Entries",
            bg="#ffb6c1",
            fg="black",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 2))  # minimal space above and just a little below

        # Entries listbox directly under the label
        self.entries_listbox = tk.Listbox(self.left_frame, width=30, height=20)  # Adjusted height
        self.entries_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))  # Allow stretching
        self.entries_listbox.bind("<<ListboxSelect>>", self.load_selected_entry)

        self.refresh_entries()

        # Frame for buttons side by side
        button_frame = tk.Frame(self.left_frame, bg="#ffb6c1")
        button_frame.pack(pady=5)

        self.new_button = tk.Button(button_frame, text="New Entry", command=self.new_entry, bg="#ff69b4", fg="white")
        self.new_button.pack(side="left", padx=(0, 5))

        self.delete_button = tk.Button(button_frame, text="Delete Entry", command=self.delete_entry, bg="#d9534f", fg="white")
        self.delete_button.pack(side="left")

    def setup_right_panel(self):
        # Title label: Arial, size 14, bold
        tk.Label(self.right_frame, text="Title", bg="#fff0f5", font=("Arial", 14, "bold")).pack(anchor="w")
        self.title_entry = tk.Entry(self.right_frame, font=("Arial", 12))
        self.title_entry.pack(fill="x", pady=(0, 10))

        # Content label: Arial, size 14, bold
        tk.Label(self.right_frame, text="Content", bg="#fff0f5", font=("Arial", 14, "bold")).pack(anchor="w")
        # Content text: Comic Sans MS, size 10, italic (slanty, readable)
        self.content_text = tk.Text(self.right_frame, font=("Comic Sans MS", 10, "italic"), height=15, wrap="word")
        self.content_text.pack(fill="both", expand=True, pady=(5, 10))

        self.save_button = tk.Button(self.right_frame, text="Save Entry", command=self.save_entry, bg="#ff69b4", fg="white")
        self.save_button.pack(anchor="e")

    def setup_bottom_panel(self):
        self.datetime_label = tk.Label(self.bottom_frame, text="", bg="#ffe6f0", font=("Arial", 10, "italic"))
        self.datetime_label.pack(anchor="w", padx=10, pady=5)

    def update_datetime_label(self, action):
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.datetime_label.config(text=f"Last {action} at: {current_time}")

    def refresh_entries(self):
        self.entries_listbox.delete(0, tk.END)
        for entry in self.manager.list_entries():
            self.entries_listbox.insert(tk.END, entry)

    def save_entry(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END)
        try:
            entry = DiaryEntry(title, content)
            entry.save()
            self.refresh_entries()
            self.update_datetime_label("saved")  # Update datetime on save
            messagebox.showinfo("Success", "Entry saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_selected_entry(self, event):
        selection = self.entries_listbox.curselection()
        if selection:
            index = selection[0]
            title = self.entries_listbox.get(index)
            content = self.manager.load_entry(title)
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, content)
            self.update_datetime_label("loaded")  # Update datetime on load

    def new_entry(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.update_datetime_label("created")  # Update datetime on new entry

    def delete_entry(self):
        selection = self.entries_listbox.curselection()
        if selection:
            index = selection[0]
            title = self.entries_listbox.get(index)
            confirm = messagebox.askyesno("Delete Entry", f"Are you sure you want to delete '{title}'?")
            if confirm:
                self.manager.delete_entry(title)
                self.refresh_entries()
                self.new_entry()

    def search_entries(self):
        query = self.search_entry.get().lower()
        self.entries_listbox.delete(0, tk.END)
        for entry in self.manager.list_entries():
            if query in entry.lower():  # Search by title
                self.entries_listbox.insert(tk.END, entry)
