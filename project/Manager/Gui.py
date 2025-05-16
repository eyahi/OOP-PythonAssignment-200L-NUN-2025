import tkinter as tk 
from tkinter import messagebox
from task_man import TaskManager

task_man = TaskManager() 

root = tk.Tk()
root.title("Task Manager")
root.geometry("400x500") 

title_label = tk.Label(root, text="Title")
title_label.pack()
title_entry = tk.Entry(root, width=40)
title_entry.pack()

desc_label = tk.Label(root, text="Description")
desc_label.pack()
desc_entry = tk.Entry(root, width=40)
desc_entry.pack()

date_label = tk.Label(root, text="Due Date (DD-MM-YYYY)")
date_label.pack()
date_entry = tk.Entry(root, width=40)
date_entry.pack()

task_listbox = tk.Listbox(root, width=70, height=15)
task_listbox.pack()

def update_task_list():
    task_listbox.delete(0, tk.END)
    for i, task in enumerate(task_man.tasks):
        task_listbox.insert(tk.END, f"{i+1}. {task.title} - {task.status}")  

def add_task():
    title = title_entry.get()
    desc = desc_entry.get()
    date = date_entry.get()
    if title and desc and date:
        task_man.add_task(title, desc, date)
        update_task_list()
        title_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def complete_task():  
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        task_man.mark_task_completed(index)
        update_task_list()  
    else:
        messagebox.showinfo("Selection Error", "Select a task to complete")

def delete_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        task_man.delete_task(index)
        update_task_list()  
    else:
        messagebox.showinfo("Selection Error", "Select a task to delete")

def view_task(event):
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        task = task_man.tasks[index]
        details = f"Title: {task.title}\n\nDescription: {task.description}\n\nDue Date: {task.due_date}\n\nStatus: {task.status}"
        messagebox.showinfo("Task Details", details)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=10)

complete_btn = tk.Button(root, text="Mark Completed", command=complete_task)
complete_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)   

task_listbox.bind("<Double-Button-1>", view_task)

update_task_list()  
root.mainloop()
