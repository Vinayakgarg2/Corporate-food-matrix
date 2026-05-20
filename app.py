from flask import Flask, render_template, request, session, redirect, Response, flash
import sqlite3
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "foodmatrix_secret"

# ---------------- UPLOAD CONFIG ----------------
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AUTO CREATE UPLOAD FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ALLOWED FILES
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    # USERS
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')

    # REQUESTS
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            meal TEXT,
            meal_date TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT,
            served INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # MENU IMAGE
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu_image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT
        )
    ''')

    conn.commit()
    conn.close()


# ---------------- GET MENU IMAGE ----------------
def get_menu_image():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("SELECT image FROM menu_image ORDER BY id DESC LIMIT 1")
    data = c.fetchone()

    conn.close()

    return data[0] if data else None


# ---------------- SEED USERS ----------------
def seed_users():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:

        c.executemany('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', [
            ("vinayak", "1234", "employee"),
            ("hr1", "1234", "hr"),
            ("admin1", "1234", "admin")
        ])

    conn.commit()
    conn.close()


# INIT
init_db()
seed_users()


# ---------------- GET REQUESTS ----------------
def get_requests():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("SELECT * FROM requests ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()
    return rows


# ---------------- STATS ----------------
def get_stats():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM requests")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'")
    pending = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM requests WHERE status='Approved'")
    approved = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM requests WHERE served=1")
    served = c.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "served": served
    }


# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('food.db')
        c = conn.cursor()

        c.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            session['role'] = user[0]

            if user[0] == "employee":
                return redirect('/employee')
            elif user[0] == "hr":
                return redirect('/hr')
            elif user[0] == "admin":
                return redirect('/admin')

        return "Invalid Login ❌"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ---------------- UPLOAD MENU ----------------
@app.route('/upload_menu', methods=['POST'])
def upload_menu():

    if session.get('role') != 'admin':
        return "Access Denied ❌"

    file = request.files.get('menu_image')

    if not file or file.filename == '':
        return "No file selected ❌"

    if not allowed_file(file.filename):
        return "Only image files allowed ❌"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(path)

    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("INSERT INTO menu_image (image) VALUES (?)", (filename,))

    conn.commit()
    conn.close()

    return redirect('/admin')


# ---------------- EMPLOYEE ----------------
@app.route('/employee', methods=['GET', 'POST'])
def employee():

    if session.get('role') != 'employee':
        return "Access Denied ❌"

    if request.method == 'POST':

        meal_type = request.form.get('meal_type')
        meal_date = request.form.get('meal_date') or ""
        start_date = request.form.get('start_date') or ""
        end_date = request.form.get('end_date') or ""

        conn = sqlite3.connect('food.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO requests
            (employee, meal, meal_date, start_date, end_date, status, served)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session['user'],
            meal_type,
            meal_date,
            start_date,
            end_date,
            "Pending",
            0
        ))

        conn.commit()
        conn.close()

        flash("Request Submitted Successfully ✅")
        return redirect('/employee')

    return render_template(
        'employee.html',
        menu_image=get_menu_image()
    )


# ---------------- HR ----------------
@app.route('/hr')
def hr():

    if session.get('role') != 'hr':
        return "Access Denied ❌"

    return render_template(
        'hr.html',
        data=get_requests(),
        stats=get_stats(),
        menu_image=get_menu_image()
    )


# ---------------- APPROVE ----------------
@app.route('/approve/<int:id>')
def approve(id):

    if session.get('role') != 'hr':
        return "Access Denied ❌"

    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("UPDATE requests SET status='Approved' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/hr')


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():

    if session.get('role') != 'admin':
        return "Access Denied ❌"

    return render_template(
        'admin.html',
        data=get_requests(),
        stats=get_stats(),
        menu_image=get_menu_image()
    )


# ---------------- SERVE ----------------
@app.route('/serve/<int:id>')
def serve(id):

    if session.get('role') != 'admin':
        return "Access Denied ❌"

    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    c.execute("UPDATE requests SET served=1 WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/admin')


# ---------------- EXPORT ----------------
@app.route('/export')
def export():

    conn = sqlite3.connect('food.db')

    df = pd.read_sql_query("SELECT * FROM requests", conn)

    file = "food_report.xlsx"
    df.to_excel(file, index=False)

    conn.close()

    return Response(
        open(file, "rb").read(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=food_report.xlsx"}
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)