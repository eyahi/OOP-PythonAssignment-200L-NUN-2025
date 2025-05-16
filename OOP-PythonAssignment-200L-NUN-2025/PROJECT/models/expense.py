from database.db import get_connection

class Expense:
    def __init__(self, user_id, description, amount, date, category_id, vendor=None):
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.vendor = vendor

    def save(self):
        """Save the expense to the database."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO expenses (user_id, description, amount, date, category_id, vendor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, self.description, self.amount, self.date, self.category_id, self.vendor))
            conn.commit()
            print("Expense added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_expenses_by_user(user_id):
        """Retrieve all expenses for a specific user."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.id, e.description, e.amount, e.date, c.name AS category, e.vendor
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = ?
        """, (user_id,))
        expenses = cursor.fetchall()
        conn.close()
        return expenses