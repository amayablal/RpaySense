import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# ✅ New Expenses table (linked by email)
c.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    note TEXT
)
''')

conn.commit()
conn.close()

print("✅ Database updated with expenses table!")
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Add a column for user_email if it doesn’t already exist
try:
    c.execute("ALTER TABLE expenses ADD COLUMN user_email TEXT")
    print("✅ user_email column added.")
except sqlite3.OperationalError:
    print("⚠️ Column already exists.")

conn.commit()
conn.close()
  