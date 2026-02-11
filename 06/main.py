import math
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.bbdd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)
ma = Marshmallow(app)


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


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class UserV2Schema(ma.SQLAlchemySchema):
    code = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()

    class Meta:
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_v2_schema = UserV2Schema()
users_v2_schema = UserV2Schema(many = True)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    importance = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(100), nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")
    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema)

    class Meta:
        model = Message
        load_instance = True
        include_fk = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


class MessageSimpleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_simple_schema = MessageSimpleSchema()
messages_simple_schema = MessageSimpleSchema(many = True)


class HealthResource(Resource):
    def get(self):
        return {
            "status": "ok",
            "v": "6",
        }


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item), 201


class UsersIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)
    
    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        user_schema.load(
            data,
            instance=item,
            partial=True,
        )
        db.session.commit()
        return user_schema.dump(item)

    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class UsersV2Resource(Resource):
    def get(self):
        items = User.query.all()
        return users_v2_schema.dump(items)
    

class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        return messages_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item), 201


class MessagesIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return message_schema.dump(item)
    
    def patch(self, id):
        item = Message.query.get_or_404(id)
        data = request.get_json()
        message_schema.load(
            data,
            instance=item,
            partial=True,
        )
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item)

    def delete(self, id):
        item = Message.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class UsersByIDMessagesResource(Resource):
    def get(self, user_id):
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 5))
        user = User.query.get_or_404(user_id)
        items = Message.query.filter_by(user = user).all()
        pages = math.ceil(len(items) / page_size)
        if page > pages:
            return {"error": "invalid page"}, 400
        return {
            "count": len(items),
            "data": messages_simple_schema.dump(items[(page - 1) * page_size : page * page_size]),
        }

    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        item = Message(**data)
        item.user = user
        db.session.add(item)
        db.session.commit()
        return message_simple_schema.dump(item), 201


api.add_resource(HealthResource, "/health")
api.add_resource(UsersResource, "/users")
api.add_resource(UsersIDResource, "/users/<int:id>")
api.add_resource(UsersV2Resource, "/users/v2")
api.add_resource(MessagesResource, "/messages")
api.add_resource(MessagesIDResource, "/messages/<int:id>")
api.add_resource(UsersByIDMessagesResource, "/users/<int:user_id>/messages")