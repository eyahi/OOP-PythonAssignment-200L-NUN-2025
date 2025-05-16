import unittest
from models.category import Category
from database.db import initialize_database, get_connection

class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        """Set up the database for testing."""
        initialize_database()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories")  # Clear test data
        conn.commit()
        conn.close()

    def test_add_category(self):
        """Test adding a category."""
        category = Category(name="Food")
        category.save()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories WHERE name = ?", ("Food",))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Food")

if __name__ == "__main__":
    unittest.main()