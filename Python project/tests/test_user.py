import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from database.db import add_user, get_user_id
from models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.username = "Victory"
        self.password = "ezioauditore"
        
        # Make sure the test user exists in the DB
        if get_user_id(self.username) is None:
            add_user(self.username, self.password)
        self.user = User("Victory", "ezioauditore")

    def test_add_expense(self):
        self.user.add_expense("Lunch", 10.0, "2025-05-01", "Food")
        self.assertEqual(len(self.user.get_expenses()), 1)

    def test_get_total_expenses(self):
        self.user.add_expense("A", 5, "2025-01-01", "Misc")
        self.user.add_expense("B", 10, "2025-01-02", "Misc")
        self.assertEqual(self.user.get_total_expenses(), 15)

if __name__ == '__main__':
    unittest.main()