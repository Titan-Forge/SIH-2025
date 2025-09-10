from flask import Flask, render_template, request, g, jsonify, send_file, redirect, url_for
import sqlite3, os, csv, io, datetime

app = Flask(__name__)
DB = "sih.db"

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
        run_id TEXT,
        slot TEXT,
        subject TEXT,
        teacher TEXT,
        room TEXT,
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
    # read form inputs
    subjects = request.form.getlist('subject')
    teachers = request.form.getlist('teacher')
    rooms = request.form.getlist('room') if request.form.getlist('room') else [None]*len(subjects)

    assigned_teachers = set()
    schedule = []
    run_id = datetime.datetime.utcnow().isoformat()

    for i, subj in enumerate(subjects):
        teacher = teachers[i] if i < len(teachers) else "TBD"
        # conflict check: if teacher already assigned in this run, mark TBD
        if teacher in assigned_teachers:
            final_teacher = "TBD"
        else:
            final_teacher = teacher
            assigned_teachers.add(teacher)
        slot = f"Period {i+1}"
        room = rooms[i] if i < len(rooms) else ""
        schedule.append({'slot': slot, 'subject': subj, 'teacher': final_teacher, 'room': room})
        # save each entry with run_id
        db = get_db()
        db.execute("INSERT INTO timetable (run_id, slot, subject, teacher, room) VALUES (?, ?, ?, ?, ?)",
                   (run_id, slot, subj, final_teacher, room))
    g._database.commit()
    return render_template("timetable.html", schedule=schedule)

@app.route('/timetable/list')
def list_tt():
    db = get_db()
    rows = db.execute("SELECT * FROM timetable ORDER BY created_at DESC LIMIT 200").fetchall()
    return render_template("timetable_list.html", rows=rows)

# JSON API endpoint
@app.route('/api/timetables')
def api_timetables():
    db = get_db()
    rows = db.execute("SELECT * FROM timetable ORDER BY created_at DESC LIMIT 200").fetchall()
    data = [dict(row) for row in rows]
    return jsonify(data)

# delete single entry
@app.route('/timetable/delete/<int:tid>', methods=['POST'])
def delete_entry(tid):
    db = get_db()
    db.execute("DELETE FROM timetable WHERE id = ?", (tid,))
    g._database.commit()
    return jsonify({"status":"ok", "deleted": tid})

# clear last run (delete by latest run_id)
@app.route('/clear_timetable', methods=['POST'])
def clear_last_run():
    db = get_db()
    row = db.execute("SELECT run_id FROM timetable ORDER BY created_at DESC LIMIT 1").fetchone()
    if row:
        run_id = row['run_id']
        db.execute("DELETE FROM timetable WHERE run_id = ?", (run_id,))
        g._database.commit()
        return jsonify({"status":"cleared", "run_id": run_id})
    return jsonify({"status":"no_data"})

# export latest run CSV
@app.route('/export_csv')
def export_csv():
    db = get_db()
    row = db.execute("SELECT run_id FROM timetable ORDER BY created_at DESC LIMIT 1").fetchone()
    if not row:
        return "No timetable to export", 404
    run_id = row['run_id']
    rows = db.execute("SELECT slot, subject, teacher, room FROM timetable WHERE run_id = ? ORDER BY id", (run_id,)).fetchall()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Slot','Subject','Teacher','Room'])
    for r in rows:
        cw.writerow([r['slot'], r['subject'], r['teacher'], r['room']])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    filename = f"timetable_{run_id}.csv"
    return send_file(output, as_attachment=True, download_name=filename, mimetype='text/csv')

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, port=port)
