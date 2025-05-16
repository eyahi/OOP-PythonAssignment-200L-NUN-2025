import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import json
import os

class Task:
    def __init__(self, title, description, deadline, priority):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority
        }

    @staticmethod
    def from_dict(data):
        return Task(data['title'], data['description'], data['deadline'], data['priority'])

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def update_task(self, index, task):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task
            self.save_tasks()

    def get_all_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(data) for data in tasks_data]
            except Exception:
                self.tasks = []

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", width=10, **kwargs):
        super().__init__(master, width=width, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = '#a0a0a0'
        self.default_fg_color = self['fg']
        self.insert('0', self.placeholder)
        self['fg'] = self.placeholder_color
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self.bind("<KeyRelease>", self._validate_digit)

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self['fg'] = self.default_fg_color

    def _add_placeholder(self, event=None):
        if not self.get():
            self['fg'] = self.placeholder_color
            self.insert(0, self.placeholder)

    def _validate_digit(self, event=None):
        value = self.get()
        if value == self.placeholder:
            return
        new_value = ''.join(filter(str.isdigit, value))
        if value != new_value:
            self.delete(0, 'end')
            self.insert(0, new_value)

    def get_value(self):
        val = self.get()
        if val == self.placeholder:
            return ""
        return val

class StylishButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = '#61afef'
        self.hover_bg = '#528bd6'
        self['bg'] = self.default_bg
        self['fg'] = '#fff'
        self['activebackground'] = self.hover_bg
        self['bd'] = 0
        self['font'] = ('Segoe UI', 11, 'bold')
        self['cursor'] = 'hand2'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_bg

    def on_leave(self, e):
        self['bg'] = self.default_bg

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#282c34")

        self.manager = TaskManager()
        self.selected_task_index = None

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        pad_y = 8
        label_fg = '#abb2bf'
        entry_bg = '#3a3f4b'
        entry_fg = '#d7dae0'
        font_label = ('Segoe UI', 10, 'bold')
        font_entry = ('Segoe UI', 10)

        self.title_label = tk.Label(self.root, text="Task Title:", fg=label_fg, bg=self.root['bg'], font=font_label)
        self.title_label.pack(anchor='w', padx=20, pady=(20,4))
        self.title_entry = tk.Entry(self.root, width=55, bg=entry_bg, fg=entry_fg, relief='flat', font=font_entry, insertbackground='white')
        self.title_entry.pack(padx=20, pady=(0,pad_y))

        self.description_label = tk.Label(self.root, text="Description:", fg=label_fg, bg=self.root['bg'], font=font_label)
        self.description_label.pack(anchor='w', padx=20, pady=(10,4))
        self.description_entry = tk.Entry(self.root, width=55, bg=entry_bg, fg=entry_fg, relief='flat', font=font_entry, insertbackground='white')
        self.description_entry.pack(padx=20, pady=(0,pad_y))

        self.deadline_label = tk.Label(self.root, text="Deadline:", fg=label_fg, bg=self.root['bg'], font=font_label)
        self.deadline_label.pack(anchor='w', padx=20, pady=(10,4))

        deadline_frame = tk.Frame(self.root, bg=self.root['bg'])
        deadline_frame.pack(padx=20, pady=(0,pad_y))

        entry_width = 6

        self.year_entry = PlaceholderEntry(deadline_frame, placeholder="YYYY", width=entry_width, bg=entry_bg, fg=entry_fg, relief='flat', font=font_entry, insertbackground='white')
        self.year_entry.pack(side='left', padx=(0,5))
        self.year_entry.bind('<KeyRelease>', lambda e: self.limit_length(self.year_entry, 4))

        slash1 = tk.Label(deadline_frame, text="/", fg=label_fg, bg=self.root['bg'], font=font_label)
        slash1.pack(side='left')

        self.month_entry = PlaceholderEntry(deadline_frame, placeholder="MM", width=entry_width, bg=entry_bg, fg=entry_fg, relief='flat', font=font_entry, insertbackground='white')
        self.month_entry.pack(side='left', padx=(5,5))
        self.month_entry.bind('<KeyRelease>', lambda e: self.limit_length(self.month_entry, 2))

        slash2 = tk.Label(deadline_frame, text="/", fg=label_fg, bg=self.root['bg'], font=font_label)
        slash2.pack(side='left')

        self.day_entry = PlaceholderEntry(deadline_frame, placeholder="DD", width=entry_width, bg=entry_bg, fg=entry_fg, relief='flat', font=font_entry, insertbackground='white')
        self.day_entry.pack(side='left', padx=(5,0))
        self.day_entry.bind('<KeyRelease>', lambda e: self.limit_length(self.day_entry, 2))

        self.priority_label = tk.Label(self.root, text="Priority:", fg=label_fg, bg=self.root['bg'], font=font_label)
        self.priority_label.pack(anchor='w', padx=20, pady=(15,4))

        self.priority_combobox = ttk.Combobox(self.root, values=["low", "medium", "high"], state="readonly", font=font_entry)
        self.priority_combobox.pack(padx=20, pady=(0,pad_y))
        self.priority_combobox.set('')

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TCombobox', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg, padding=5, bordercolor=entry_bg, borderwidth=0, relief='flat')

        buttons_frame = tk.Frame(self.root, bg=self.root['bg'])
        buttons_frame.pack(pady=15)

        self.add_task_button = StylishButton(buttons_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side='left', padx=8, ipadx=8, ipady=6)

        self.edit_task_button = StylishButton(buttons_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(side='left', padx=8, ipadx=8, ipady=6)
        self.edit_task_button.config(state='disabled')

        self.delete_task_button = StylishButton(buttons_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(side='left', padx=8, ipadx=8, ipady=6)
        self.delete_task_button.config(state='disabled')

        self.selected_label = tk.Label(self.root, text="Selected Task: None", fg=label_fg, bg=self.root['bg'], font=('Segoe UI', 10, 'italic'))
        self.selected_label.pack(padx=20, anchor='w')

        tree_frame = tk.Frame(self.root, bg=self.root['bg'])
        tree_frame.pack(padx=20, pady=10, fill='both', expand=True)

        columns = ("Title", "Description", "Deadline", "Priority")
        self.task_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.task_tree.heading(col, text=col)
            # Set column widths appropriately
            if col == "Title":
                self.task_tree.column(col, width=150, anchor='w')
            elif col == "Description":
                self.task_tree.column(col, width=300, anchor='w')
            elif col == "Deadline":
                self.task_tree.column(col, width=100, anchor='center')
            elif col == "Priority":
                self.task_tree.column(col, width=80, anchor='center')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
            background="#21252b",
            foreground="#abb2bf",
            rowheight=25,
            fieldbackground="#282c34",
            font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', '#61afef')], foreground=[('selected', '#000000')])

        self.task_tree.pack(fill='both', expand=True)

        self.task_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def limit_length(self, entry_widget, max_len):
        text = entry_widget.get_value()
        if len(text) > max_len:
            entry_widget.delete(max_len, 'end')

    def validate_inputs(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        year = self.year_entry.get_value()
        month = self.month_entry.get_value()
        day = self.day_entry.get_value()
        priority = self.priority_combobox.get()

        if not title:
            messagebox.showerror("Input Error", "Please enter a task title.")
            return None

        if not (year and month and day):
            messagebox.showerror("Input Error", "Please enter a complete deadline (Year/Month/Day).")
            return None

        if not priority:
            messagebox.showerror("Input Error", "Please select a priority.")
            return None

        try:
            year_i = int(year)
            month_i = int(month)
            day_i = int(day)
            datetime(year_i, month_i, day_i)
        except ValueError:
            messagebox.showerror("Input Error", "The deadline date you entered is not valid.")
            return None

        deadline_str = f"{year_i:04d}-{month_i:02d}-{day_i:02d}"
        return Task(title, description, deadline_str, priority)

    def add_task(self):
        task = self.validate_inputs()
        if task:
            self.manager.add_task(task)
            messagebox.showinfo("Success", "Task added successfully!")
            self.clear_entries()
            self.refresh_task_list()

    def edit_task(self):
        if self.selected_task_index is None:
            return
        task = self.validate_inputs()
        if task:
            self.manager.update_task(self.selected_task_index, task)
            messagebox.showinfo("Success", "Task updated successfully!")
            self.clear_entries()
            self.refresh_task_list()

    def delete_task(self):
        if self.selected_task_index is not None:
            self.manager.delete_task(self.selected_task_index)
            messagebox.showinfo("Success", "Task deleted successfully!")
            self.clear_entries()
            self.refresh_task_list()

    def clear_entries(self):
        self.title_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.month_entry.delete(0, 'end')
        self.day_entry.delete(0, 'end')
        self.priority_combobox.set('')
        self.edit_task_button.config(state='disabled')
        self.delete_task_button.config(state='disabled')
        self.selected_label.config(text="Selected Task: None")
        self.selected_task_index = None
        self.task_tree.selection_remove(self.task_tree.selection())

    def on_tree_select(self, event):
        selected = self.task_tree.selection()
        if selected:
            index = int(selected[0])  # use iid as index string
            self.selected_task_index = index
            task = self.manager.get_all_tasks()[index]
            # Fill form entries
            self.title_entry.delete(0, 'end')
            self.title_entry.insert(0, task.title)
            self.description_entry.delete(0, 'end')
            self.description_entry.insert(0, task.description)
            year, month, day = task.deadline.split('-')
            self.year_entry.delete(0, 'end')
            self.year_entry.insert(0, year)
            self.month_entry.delete(0, 'end')
            self.month_entry.insert(0, month)
            self.day_entry.delete(0, 'end')
            self.day_entry.insert(0, day)
            self.priority_combobox.set(task.priority)
            self.edit_task_button.config(state='normal')
            self.delete_task_button.config(state='normal')
            self.selected_label.config(text=f"Selected Task: {task.title}")
        else:
            self.clear_entries()

    def refresh_task_list(self):
        self.task_tree.delete(*self.task_tree.get_children())
        for idx, task in enumerate(self.manager.get_all_tasks()):
            # Insert with iid as index string for easy reference
            self.task_tree.insert('', 'end', iid=str(idx), values=(task.title, task.description, task.deadline, task.priority))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

