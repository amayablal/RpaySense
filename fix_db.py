import sqlite3

# ✅ Connect to your existing database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# ✅ Add the missing column (ONLY runs once)
try:
    c.execute("ALTER TABLE expenses ADD COLUMN user_email TEXT;")
    print("✅ user_email column added successfully!")
except sqlite3.OperationalError:
    print("⚠️ Column already exists. Skipping...")

conn.commit()
conn.close()

