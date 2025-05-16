from models.task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def display_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
        else:
            print("\nTasks:")
            for idx, task in enumerate(self.tasks):
                print(f"{idx + 1}. {task}")

    def get_tasks_by_priority(self, level):
        return [task for task in self.tasks if task.priority.lower() == level.lower()]

    def get_tasks_by_deadline(self, date):
        return [task for task in self.tasks if task.deadline == date]
