from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    subjects = request.form.getlist('subject')
    teachers = request.form.getlist('teacher')

    # Simple timetable logic (just pairing for now)
    schedule = []
    for i in range(len(subjects)):
        schedule.append({
            "slot": f"Period {i+1}",
            "subject": subjects[i],
            "teacher": teachers[i]
        })

    return render_template("timetable.html", schedule=schedule)

if __name__ == "__main__":
    app.run(debug=True)

