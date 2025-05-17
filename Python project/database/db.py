import sqlite3
import bcrypt
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "expense_tracker.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    return False

def get_user_id(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_expense_to_db(user_id, expense):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (id, user_id, description, amount, date, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        expense.id,
        user_id,
        expense.description,
        expense.amount,
        expense.date,
        expense.category
    ))
    conn.commit()
    conn.close()
    #

def update_expense_in_db(expense):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET description = ?, amount = ?, date = ?, category = ?
        WHERE id = ?
    """, (expense.description, expense.amount, expense.date, expense.category, expense.id))
    conn.commit()
    conn.close()

def get_expenses_by_user_id(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, description, amount, date, category
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense_by_id(expense_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    results = cursor.fetchall()
    conn.close()
    return results


def edit_category(old_name, new_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET category = ? WHERE category = ?", (new_name, old_name))
    conn.commit()
    conn.close()

def delete_category(category_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE category = ?", (category_name,))
    conn.commit()
    conn.close()
    #

   