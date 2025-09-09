from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3
import os

DB = "sih.db"
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot TEXT,
        subject TEXT,
        teacher TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = sqlite3.connect(DB)
    conn.executescript(sql)
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    subjects = request.form.getlist('subject')
    teachers = request.form.getlist('teacher')

    schedule = []
    for i, s in enumerate(subjects):
        t = teachers[i] if i < len(teachers) else "TBD"
        slot = f"Period {i+1}"
        schedule.append({'slot': slot, 'subject': s, 'teacher': t})
        # save to DB
        db = get_db()
        db.execute("INSERT INTO timetable (slot, subject, teacher) VALUES (?, ?, ?)", (slot, s, t))
    g._database.commit()

    return render_template("timetable.html", schedule=schedule)

@app.route('/timetable/list')
def list_tt():
    db = get_db()
    rows = db.execute("SELECT * FROM timetable ORDER BY created_at DESC").fetchall()
    return render_template("timetable_list.html", rows=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
