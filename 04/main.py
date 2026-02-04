from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bbdd.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(11), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return "<User: {}>".format(self.id)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")
    def __repr__(self):
        return "<Message: {}>".format(self.id)


@app.route("/")
def view_root():
    return {}


@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": "4"
    }


@app.route("/users")
def users():
    data = User.query.all()
    return render_template("users.html", items=data)


@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users_add.html")
    if request.method == "POST":
        item = User(
            code=request.form["code"],
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("users_add.html", information="Changes saved")


# Read    /users/<id>/ => muestra datos de un usuario con el id
# Update  /users/<id>/edit/ => actualizar datos de un usuarios (formulario)
# Delete  /users/<id>/delete/ => pregunte si vas a borrar