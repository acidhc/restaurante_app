# restaurante_app/database.py
import sqlite3

def create_tables():
    with sqlite3.connect('restaurant.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            price REAL NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tables (
                            id INTEGER PRIMARY KEY,
                            items TEXT,
                            total REAL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL,
                            total REAL NOT NULL
                        )''')

if __name__ == "__main__":
    create_tables()
