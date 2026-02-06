from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.bbdd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


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
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    importance = db.Column(db.String(100), nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")
    def __repr__(self):
        return "<Message: {}>".format(self.id)


class HealthResource(Resource):
    def get(self):
        return {
            "status": "ok",
            "v": "6",
        }


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        data = []
        for x in items:
            data.append({
                "id": x.id,
                "code": x.code,
                "first_name": x.first_name,
                "last_name": x.last_name,
                "age": x.age,
            })
        return data

    def post(self):
        data = request.get_json()
        item = User(
            code=data["code"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
        )
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "code": item.code,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
        }, 201


class UsersIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return {
            "id": item.id,
            "code": item.code,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
        }
    
    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        item.code = data.get("code", item.code)
        item.first_name = data.get("first_name", item.first_name)
        item.last_name = data.get("last_name", item.last_name)
        item.age = data.get("age", item.age)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "code": item.code,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
        }

    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        data = []
        for x in items:
            data.append({
                "id": x.id,
                "title": x.title,
                "content": x.content,
                "importance": x.importance,
                "user_id": x.user_id,
            })
        return data

    def post(self):
        data = request.get_json()
        item = Message(
            title=data["title"],
            content=data["content"],
            importance=data["importance"],
            user_id=data["user_id"],
        )
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "importance": item.importance,
            "user_id": item.user_id,
        }, 201


api.add_resource(HealthResource, "/health")
api.add_resource(UsersResource, "/users")
api.add_resource(UsersIDResource, "/users/<int:id>")
api.add_resource(MessagesResource, "/messages")


## LABORATORIO
## messages (priority => nuevo campo)
##    flask --app main db migrate
#     flask --app main db upgrade
## /messages/<id> REST
##   GET => { id: 1, .... }
##   PATCH ({title: 1234}) => { id: 1, ... }
##   DELETE => {}