import sqlite3

DB_NAME = "expenses.db"

def init_db():
    """Create expenses table if not exists"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_expense(amount, category, date, note=""):
    """Insert new expense"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (amount, category, date, note)
        VALUES (?, ?, ?, ?)
    """, (amount, category, date, note))
    conn.commit()
    conn.close()

def get_all_expenses():
    """Fetch all records"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows