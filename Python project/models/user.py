import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.expense import Expense
from database.db import add_expense_to_db, connect_db, get_user_id

class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__expenses = []

    def add_expense(self, description, amount, date, category):
        expense = Expense(description, amount, date, category)
        self.__expenses.append(expense)

        user_id = get_user_id(self.__username)
        if user_id:
            add_expense_to_db(user_id, expense)
        else:
            print("Error: User ID not found. Expense not saved to DB.")

    def get_total_expenses(self):
        return sum(exp.amount for exp in self.__expenses)

    def get_expenses(self):
        return self.__expenses
       #
    
    def get_expenses_by_user_id(user_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, description, amount, date, category
            FROM expenses
            WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_expense_by_id(self, expense_id):
        for exp in self.__expenses:
            if exp.id ==   expense_id:
                return exp
        return None

    def edit_expense_by_id(self, expense_id, description=None, amount=None, date=None, category=None):
        expense = self.get_expense_by_id(expense_id)
        if expense:
            expense.edit_expense(description, amount, date, category)
            return True
        return False

    def delete_expense_by_id(self, expense_id):
        self.__expenses = [exp for exp in self.__expenses if exp.id != expense_id]

        #