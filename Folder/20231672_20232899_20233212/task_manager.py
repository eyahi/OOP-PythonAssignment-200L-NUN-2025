import tkinter as tk
from tkinter import messagebox
import json
import os

# Task class: defines what a task is


class Task:
    def __init__(self, title, description, deadline, priority, status="Pending"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def mark_done(self):
        self.status = "Completed"

# Handles storing and loading tasks from a file


class TaskManager:
    def __init__(self):
        self.file = "tasks.json"
        self.tasks = self.load_tasks()

    def add(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def save_tasks(self):
        with open(self.file, "w") as f:
            json.dump([task.__dict__ for task in self.tasks], f)

    def load_tasks(self):
        if not os.path.exists(self.file):
            return []
        with open(self.file, "r") as f:
            return [Task(**data) for data in json.load(f)]

# The main app with the buttons and boxes


class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Task Manager")
        self.root.configure(bg="#f0f4f8")
        self.manager = TaskManager()

        self.create_ui()
        self.show_tasks()

    def create_ui(self):
        # Input fields
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(pady=10)

        tk.Label(frame, text="Title:", bg="#f0f4f8").grid(row=0, column=0)
        self.title = tk.Entry(frame, width=40)
        self.title.grid(row=0, column=1)

        tk.Label(frame, text="Description:",
                 bg="#f0f4f8").grid(row=1, column=0)
        self.desc = tk.Entry(frame, width=40)
        self.desc.grid(row=1, column=1)

        tk.Label(frame, text="Deadline:", bg="#f0f4f8").grid(row=2, column=0)
        self.deadline = tk.Entry(frame, width=40)
        self.deadline.grid(row=2, column=1)

        tk.Label(frame, text="Priority:", bg="#f0f4f8").grid(row=3, column=0)
        self.priority = tk.Entry(frame, width=40)
        self.priority.grid(row=3, column=1)

        tk.Button(frame, text="Add Task", bg="#5DADE2", fg="white",
                  command=self.add_task).grid(row=4, column=1, sticky=tk.E, pady=5)

        # Task list
        self.task_list = tk.Listbox(self.root, width=60, height=10)
        self.task_list.pack(pady=10)

        # Action buttons
        btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        btn_frame.pack()

        tk.Button(btn_frame, text="Mark Done", bg="#58D68D", fg="white",
                  command=self.complete_task).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete Task", bg="#EC7063", fg="white",
                  command=self.delete_task).pack(side=tk.LEFT, padx=10)

    def add_task(self):
        title = self.title.get()
        desc = self.desc.get()
        deadline = self.deadline.get()
        priority = self.priority.get()

        if title and deadline and priority:
            task = Task(title, desc, deadline, priority)
            self.manager.add(task)
            self.show_tasks()
            self.clear_fields()
        else:
            messagebox.showwarning(
                "Missing Info", "Please fill in Title, Deadline, and Priority")

    def clear_fields(self):
        self.title.delete(0, tk.END)
        self.desc.delete(0, tk.END)
        self.deadline.delete(0, tk.END)
        self.priority.delete(0, tk.END)

    def show_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.manager.tasks:
            self.task_list.insert(tk.END, f"â¢ {task.title} ({
                                  task.priority}) - {task.deadline} [{task.status}]")

    def complete_task(self):
        selected = self.task_list.curselection()
        if selected:
            index = selected[0]
            self.manager.tasks[index].mark_done()
            self.manager.save_tasks()
            self.show_tasks()

    def delete_task(self):
        selected = self.task_list.curselection()
        if selected:
            self.manager.remove(selected[0])
            self.show_tasks()


# Start the app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("550x450")
    app = TaskApp(root)
    root.mainloop()
