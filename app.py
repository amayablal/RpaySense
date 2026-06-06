from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'Amayablal@2006'

DB_NAME = "users.db"

# ✅ Create tables if they don't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
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

    # Expenses table
    c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        date TEXT,
        amount REAL,
        category TEXT,
        note TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ✅ Home Page
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE user_email = ?", (email,))
    expenses = c.fetchall()
    conn.close()

    return render_template('index.html', expenses=expenses)

# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# ✅ Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ✅ Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                      (username, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="User with that email already exists")

    return render_template('signup.html')

# ✅ Add Expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user' not in session:
        return redirect(url_for('login'))

    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    note = request.form['note']
    email = session['user']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO expenses (date, amount, category, note, user_email) VALUES (?, ?, ?, ?, ?)',
              (date, amount, category, note, email))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# ✅ Delete Expense
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ? AND user_email = ?", (expense_id, email))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
