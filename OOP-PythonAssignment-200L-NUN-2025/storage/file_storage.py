import json
import os
from models.task import Task

class FileStorage:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def save_tasks(self, tasks):
        """
        Saves a list of Task objects to a JSON file.
        """
        try:
            with open(self.filename, 'w') as f:
                data = [task.__dict__ for task in tasks]
                json.dump(data, f, indent=4)
            print(f"✅ Saved {len(tasks)} tasks to {self.filename}")
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")

    def load_tasks(self):
        """
        Loads tasks from a JSON file and returns a list of Task objects.
        """
        if not os.path.exists(self.filename):
            print(f"⚠️ File '{self.filename}' not found. Starting with an empty task list.")
            return []

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task(**task_data) for task_data in data]
        except Exception as e:
            print(f"❌ Error loading tasks: {e}")
            return []
