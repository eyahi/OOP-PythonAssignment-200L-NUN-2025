import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from models.expense import Expense

class TestExpense(unittest.TestCase):
    def test_create_expense(self):
        e = Expense("Lunch", 12.5, "2025-05-10", "Food")
        self.assertEqual(e.description, "Lunch")
        self.assertEqual(e.amount, 12.5)
        self.assertEqual(e.date, "2025-05-10")
        self.assertEqual(e.category, "Food")

if __name__ == '__main__':
    unittest.main()
