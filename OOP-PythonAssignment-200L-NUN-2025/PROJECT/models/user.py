import bcrypt
from database.db import get_connection

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def hash_password(password):
        """Hash a plain-text password."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a plain-text password against a hashed password."""
        return bcrypt.checkpw(password.encode(), hashed_password)

    def save(self):
        """Save the user to the database."""
        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = User.hash_password(self.password)
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, hashed_password))
            conn.commit()
            print(f"User '{self.username}' registered successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def authenticate(username, password):
        """Authenticate a user by username and password."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and User.verify_password(password, result[0]):
            print(f"User '{username}' logged in successfully!")
            return True
        else:
            print("Invalid username or password!")
            return False
