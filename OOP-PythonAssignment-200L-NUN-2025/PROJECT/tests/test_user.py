import unittest
from models.user import User
from database.db import initialize_database, get_connection

class TestUserModel(unittest.TestCase):
    def setUp(self):
        """Set up the database for testing."""
        initialize_database()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")  # Clear test data
        conn.commit()
        conn.close()

    def test_user_registration(self):
        """Test user registration."""
        user = User(username="testuser", password="password123")
        user.save()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", ("testuser",))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "testuser")

    def test_user_authentication(self):
        """Test user authentication."""
        user = User(username="testuser", password="password123")
        user.save()

        self.assertTrue(User.authenticate("testuser", "password123"))
        self.assertFalse(User.authenticate("testuser", "wrongpassword"))

if __name__ == "__main__":
    unittest.main()