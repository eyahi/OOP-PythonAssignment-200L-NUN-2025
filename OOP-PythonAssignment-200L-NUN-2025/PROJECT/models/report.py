import matplotlib.pyplot as plt
from database.db import get_connection

class Report:
    @staticmethod
    def generate_pie_chart(user_id):
        """Generate a pie chart showing spending percentages by category for the logged-in user."""
        conn = get_connection()
        cursor = conn.cursor()

    # Query to calculate total spending by category for the logged-in user
        cursor.execute("""
        SELECT c.name AS category, SUM(e.amount) AS total_spent
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.user_id = ?
        GROUP BY c.name
        """, (user_id,))

        data = cursor.fetchall()
        conn.close()

        if not data:
            return False  # No data available

        # Prepare data for the pie chart
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        # Generate the pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title("Spending Breakdown by Category")
        plt.show(block=False)  # Non-blocking mode

        return True