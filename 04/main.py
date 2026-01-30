from flask import Flask
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