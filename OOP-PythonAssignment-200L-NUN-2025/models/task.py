class Task:
    def __init__(self, title, description, deadline, priority, status="pending"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def mark_as_completed(self):
        self.status = "completed"

    def edit_task(self, title=None, description=None, deadline=None, priority=None, status=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = deadline
        if priority is not None:
            self.priority = priority
        if status is not None:
            self.status = status

    def __str__(self):
        return f"{self.title} | {self.description} | {self.deadline} | {self.priority} | {self.status}"
