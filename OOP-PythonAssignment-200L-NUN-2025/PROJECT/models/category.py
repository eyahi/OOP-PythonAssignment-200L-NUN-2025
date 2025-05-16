from database.db import get_connection

class Category:
    def __init__(self, name):
        self.name = name

    def save(self):
        """Save the category to the database."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (self.name,))
            conn.commit()
            print(f"Category '{self.name}' added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_all_categories():
        """Retrieve all categories from the database."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()
        return categories