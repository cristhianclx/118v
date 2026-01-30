from flask import Flask


app = Flask(__name__)


@app.route("/")
def view_root():
    return "<p>Hello, World</p>"


@app.route("/ct")
def view_ct():
    return "<p>ct</p>"


@app.route("/students")
def view_messages():
    return [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]


@app.route("/students/<id_student>/abc/<id_curso>")
def view_messages_by_student(id_student, id_curso):
    return {"id": id_student, "name": "A"}


data = [
    { "id": 1, "name": "A", "score": 88 },
    { "id": 5, "name": "G", "score": 50 },
    { "id": 10, "name": "Y", "score": 92 },
]


# /students-by-score/50/99
# [{ "id": 5, "name": "G", "score": 50 }, { "id": 10, "name": "Y", "score": 92 }]