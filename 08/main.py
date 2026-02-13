from flask import Flask

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cibertec"

jwt = JWTManager(app)


@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": "8"
    }


@app.route("/public")
def view_public():
    return {
        "id": 1,
        "name": "cristhian"
    }


@app.route("/private")
@jwt_required()
def view_private():
    return {
        "id": 1,
        "name": "cristhian",
        "dni": 12345678,
        "address": "jr lima 123"
    }


@app.route("/me")
@jwt_required()
def view_me():
    user_logged = get_jwt_identity()
    return {
        "data": user_logged
    }


@app.route("/login", methods=["POST"])
def view_login():
    access_token = create_access_token(identity = "cristhian")
    return {
        "access_token": access_token
    }