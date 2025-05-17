import uuid

class Expense:
    def __init__(self, description, amount, date, category):
        self.id = str(uuid.uuid4())
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category

    def edit_expense(self, description=None, amount=None, date=None, category=None):
        if description is not None:
            self.description = description
        if amount is not None:
            self.amount = amount
        if date is not None:
            self.date = date
        if category is not None:
            self.category = category