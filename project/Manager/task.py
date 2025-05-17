from datetime import datetime
class Task: 
    def __init__(self, title, description, due_date, status="Pending") : 
        self.title = title
        self.description = description 
        self.due_date = due_date # Expected in "DD-MM-YYYY" format
        self.status = status # Default is "Pending" 
    def mark_as_completed(self):   
        self.status = "Completed"
    def update_task(self, title=None, description=None, due_date=None):
        if title:
            self.title = title 
        if description: 
            self.description = description
        if due_date: 
            self.due_date = due_date
    def str(self):
        return (f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Due Date: {self.due_date}\n"
                f"Status: {self.status}")
