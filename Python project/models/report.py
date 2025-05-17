import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt
from database.db import get_user_id, connect_db

class Report:
    def __init__(self, username):
        self.username = username
        self.user_id = get_user_id(username)

    def get_category_summary(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", (self.user_id,))
        summary = cursor.fetchall()
        conn.close()
        return summary

    def generate_category_report(self):
        data = self.get_category_summary()
        if not data:
            print("No expense data found.")
            return
        categories, totals = zip(*data)
        plt.figure(figsize=(8,6))
        plt.bar(categories, totals, color='skyblue')
        plt.title(f"Total Expenses by Category - {self.username}")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.tight_layout()
        plt.show()

    def generate_pie_chart(self):
        data = self.get_category_summary()
        if not data:
            print("No expense data found.")
            return
        categories, totals = zip(*data)
        plt.figure(figsize=(7,7))
        plt.pie(totals, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title(f"Spending Breakdown - {self.username}")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    from database.db import create_tables
    create_tables()

    username = input("Enter username for report: ")
    report = Report(username)

    report.generate_category_report()
    report.generate_pie_chart()
