from task import Task
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date):
        task = Task(title, description, due_date)
        self.tasks.append(task)

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"Task {i}:\n{task}")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            print("Task deleted.")
        else:
            print("Invalid task index.")

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_as_completed()
            print("Task marked as completed.")
        else:
            print("Invalid task index.")

    def search_task_by_title(self, keyword):
        results = [task for task in self.tasks if keyword.lower() in task.title.lower()]
        if results:
            for task in results: 
             print(task)
        else: 
          print("No task found with that keyword.")
if __name__=="__main__":
    tm = TaskManager()
    
if __name__ == "__main__":
    tm = TaskManager()
    
    print("\n--- Task Manager ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Search Task by Title")
    print("6. Exit")
        
    choice = input("Enter your choice (1-6): ")
        
    if choice == "1":
        title = input("Enter task: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (DD-MM-YYYY): ")
        tm.add_task(title, description, due_date)
    elif choice == "2":
        tm.display_tasks()
    elif choice == "3":
        tm.display_tasks()
        index = int(input("Enter task number to mark as completed: ")) - 1
        tm.mark_task_completed(index)
    elif choice == "4":
        tm.display_tasks()
        index = int(input("Enter task number to delete: ")) - 1
        tm.delete_task(index)
    elif choice == "5":
        keyword = input("Enter keyword to search in task titles: ")
        tm.search_task_by_title(keyword)
    elif choice == "6":
        print("Exiting Task Manager. Goodbye!")
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")

    