from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create database and table
def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            return redirect('/login')
        except sqlite3.IntegrityError:
            return 'User already exists!'
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
            user = cur.fetchone()
            if user:
                session['email'] = email
                return redirect('/welcome')
            else:
                error = 'Invalid email or password.'
    return render_template('login.html', error=error)


@app.route('/welcome')
def welcome():
    if 'email' not in session:
        return redirect('/login')
    username = session['email'].split('@')[0]
    return render_template('welcome.html', username=username)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0",port=8080,debug=True)
