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


api.add_resource(HealthResource, "/health")
api.add_resource(UsersResource, "/users")


##
## crear la tabla message (04) (id, title*, content, importance*, user_id, user, created)
## correr la migracion
##    flask --app main db migrate # crea la migracion
##    flask --app main db upgrade # aplicar la migracion
## REST = /messages/
##          GET =>
##          POST =>
##









"""
  /users/<id>
    GET:
      parametros: -
      response: { id: 1, first: aaa, last: bbb}
      status response: 200
    PATCH/PUT:
      parametros: { last: ccc}
      response: { id: 1, first: aaa, last: ccc }
      status response: 200
    DELETE:
      parametros: -
      response: -
      status response: 204 # algo paso pero no tengo nada que devolver
 """