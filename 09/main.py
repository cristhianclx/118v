from flask import Flask, render_template
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

socketio = SocketIO(app)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return "<Message: {}>".format(self.id)
    

@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": "9"
    }


@app.route("/")
def view_home():
    items = Message.query.all()
    return render_template("home.html", items=items)


@socketio.on("ws-welcome")
def handle_ws_welcome(data, methods=["GET", "POST"]):
    print("received: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data, methods=["GET", "POST"]):
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    socketio.emit("ws-messages-responses", data)


# LABORATORIO
# marshmallow (message)
# message (priority)
# mensaje (visualizacion) - created
# mensaje (visualizacion) - priority high (poner en color rojo)