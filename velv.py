from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, g, send_from_directory
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

DATABASE = 'users.db'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join('templates', 'uploads')  # Adjust path as needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/community3')
def community3():
    post_id = request.args.get('id')
    db = get_db()
    cur = db.execute('SELECT id, title, content, image FROM posts WHERE id = ?', (post_id,))
    post = cur.fetchone()

    post_data = {
        'id': post['id'],
        'title': post['title'],
        'content': post['content'],
        'image': post['image']
    } if post else None

    return render_template('community3.html', post=post_data)

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_posts')
def get_posts():
    db = get_db()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return jsonify([dict(post) for post in posts])

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
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password-check']
        if not all([name, tel, email, password, password_check]):
            return 'All fields are required', 400
        if password != password_check:
            return 'Passwords do not match', 400
        db = get_db()
        if db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone():
            return 'Email already registered', 400
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (name, tel, email, password) VALUES (?, ?, ?, ?)", (name, tel, email, hashed_password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('index'))

@app.route('/community')
def community():
    if 'user_id' in session:
        return render_template('community.html')
    return redirect(url_for('login'))

@app.route('/community2', methods=['GET', 'POST'])
def community2():
    if 'user_id' in session:
        if request.method == 'POST':
            author = session['user_name']
            title = request.form['title']
            content = request.form['content']
            date = request.form.get('date', '2023-05-01')
            views = request.form.get('views', 0)
            image = request.files['image']
            
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            if image and allowed_file(image.filename):
                filename = str(uuid.uuid4()) + secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = 'uploads/' + filename  # Ensure relative path is stored correctly
            else:
                image_path = None

            db = get_db()
            db.execute("INSERT INTO posts (author, title, content, date, views, image) VALUES (?, ?, ?, ?, ?, ?)",
                       (author, title, content, date, views, image_path))
            db.commit()
            flash('Post successfully submitted!')
            return redirect(url_for('community'))
        return render_template('community2.html')
    return redirect(url_for('login'))


@app.route('/submit_post', methods=['POST'])
def submit_post():
    if 'user_id' in session:
        author = session['user_name']
        title = request.form['title']
        content = request.form['content']
        date = request.form.get('date', '2023-05-01')
        views = request.form.get('views', 0)
        db = get_db()
        db.execute("INSERT INTO posts (author, title, content, date, views) VALUES (?, ?, ?, ?, ?)", (author, title, content, date, views))
        db.commit()
        flash('Post successfully submitted!')
        return redirect(url_for('community'))
    return redirect(url_for('login'))

@app.route('/view_post')
def view_post():
    post_id = request.args.get('id')
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post:
        post_data = dict(post)
        return render_template('view_post.html', post=post_data)
    else:
        return "Post not found", 404

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/page10')
def page10():
    return render_template('page10.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
