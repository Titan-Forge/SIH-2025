from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # read form inputs
    subjects = request.form.getlist('subject')   # form fields named subject[]
    teachers = request.form.getlist('teacher')  # form fields named teacher[]
    # VERY simple dummy scheduler: pair subject[i] -> teacher[i]
    schedule = []
    for i, s in enumerate(subjects):
        schedule.append({'slot': f'Slot {i+1}', 'subject': s, 'teacher': teachers[i] if i < len(teachers) else 'TBD'})
    return render_template('timetable.html', schedule=schedule)  # create timetable.html next

