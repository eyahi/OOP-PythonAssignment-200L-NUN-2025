import unittest
from models.expense import Expense
from models.category import Category
from models.report import Report
from database.db import initialize_database, get_connection

class TestReportModel(unittest.TestCase):
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

    def test_generate_outbreak_map(self):
        """Test generating the outbreak map."""
        expense = Expense(user_id=1, description="Lunch", amount=15.50, date="2025-05-11", category_id=1, vendor="UberEats")
        expense.save()

        # This test will not assert but will ensure no errors occur during map generation
        Report.generate_outbreak_map(user_id=1)

if __name__ == "__main__":
    unittest.main()