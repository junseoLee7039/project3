from flask import Flask, render_template, request, redirect, session,url_for
import os
import sqlite3
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'users.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if c.fetchone() is None:
            with app.open_resource('schema.sql', mode='r') as f:    
                db.cursor().executescript(f.read())
                db.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['mail']
        password = request.form['password']
        password_check = request.form['password-check']
        if not name or not tel or not email or not password or not password_check:
            return 'All fields are required', 400
        if password != password_check:
            return 'Passwords do not match', 400
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        if c.fetchone() is not None:
            return 'Email already registered', 400

        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (name, tel, email, password) VALUES (?, ?, ?, ?)", (name, tel, email, hashed_password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

from flask import Flask, render_template, request, redirect, session,url_for
import os
import sqlite3
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'users.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:    
            db.cursor().executescript(f.read())
            db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['mail']
        password = request.form['password']
        password_check = request.form['password-check']
        if not name or not tel or not email or not password or not password_check:
            return 'All fields are required', 400
        if password != password_check:
            return 'Passwords do not match', 400
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        if c.fetchone() is not None:
            return 'Email already registered', 400

        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (name, tel, email, password) VALUES (?, ?, ?, ?)", (name, tel, email, hashed_password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['jdk']
        password = request.form['password']

        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        if user is not None and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
