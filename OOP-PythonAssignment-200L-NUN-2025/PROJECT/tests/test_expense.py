import unittest
from models.expense import Expense
from database.db import initialize_database, get_connection

class TestExpenseModel(unittest.TestCase):
    def setUp(self):
        """Set up the database for testing."""
        initialize_database()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")  # Clear test data
        cursor.execute("DELETE FROM categories")  # Clear test data
        cursor.execute("DELETE FROM users")  # Clear test data
        cursor.execute("INSERT INTO categories (id, name) VALUES (1, 'Food')")  # Add test category
        cursor.execute("INSERT INTO users (id, username, password) VALUES (1, 'testuser', 'password123')")  # Add test user
        conn.commit()
        conn.close()

    def test_add_expense(self):
        """Test adding an expense."""
        expense = Expense(user_id=1, description="Lunch", amount=15.50, date="2025-05-11", category_id=1, vendor="UberEats")
        expense.save()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT description, amount FROM expenses WHERE description = ?", ("Lunch",))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Lunch")
        self.assertEqual(result[1], 15.50)

if __name__ == "__main__":
    unittest.main()