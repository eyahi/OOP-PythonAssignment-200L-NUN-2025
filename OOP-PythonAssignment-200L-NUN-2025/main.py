from models.task import Task
from models.task_manager import TaskManager
from datetime import datetime

def display_menu():
    print("\n" + "="*40)
    print("       🚀 Task Manager 🚀       ")
    print("="*40)
    print("1. Add Task")
    print("2. Display Tasks")
    print("3. Exit")
    print("="*40)

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            # Try to parse date in format YYYY-MM-DD
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_str
        except ValueError:
            print("❌ Invalid date format. Please enter date as YYYY-MM-DD.")

def get_valid_priority(prompt):
    valid_priorities = ['low', 'medium', 'high']
    while True:
        priority = input(prompt).strip().lower()
        if priority in valid_priorities:
            return priority
        else:
            print(f"❌ Invalid priority. Please choose from {valid_priorities}.")

def get_task_details():
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    deadline = get_valid_date("Enter task deadline (YYYY-MM-DD): ")
    priority = get_valid_priority("Enter task priority (low, medium, high): ")
    return title, description, deadline, priority

def main():
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            try:
                title, description, deadline, priority = get_task_details()
                task = Task(title=title, description=description, deadline=deadline, priority=priority)
                manager.add_task(task)
                print("\n✅ Task added successfully.")
            except Exception as e:
                print(f"\n❌ Error adding task: {e}")

        elif choice == '2':
            try:
                tasks = manager.get_all_tasks() if hasattr(manager, 'get_all_tasks') else None
                if tasks is None or len(tasks) == 0:
                    print("\n📭 No tasks to display.")
                else:
                    print("\n" + "="*40)
                    print("Current Tasks:")
                    for idx, task in enumerate(tasks, 1):
                        print(f"\nTask #{idx}")
                        print(f" Title      : {task.title}")
                        print(f" Description: {task.description}")
                        print(f" Deadline   : {task.deadline}")
                        print(f" Priority   : {task.priority.capitalize()}")
                    print("="*40)
            except Exception as e:
                print(f"\n❌ Error displaying tasks: {e}")

        elif choice == '3':
            print("\n👋 Exiting the Task Manager. Goodbye!\n")
            break

        else:
            print("\n❌ Invalid choice. Please select a valid option (1-3).")

if __name__ == "__main__":
    main()

