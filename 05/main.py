from flask import Flask
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)


class HealthResource(Resource):
    def get(self):
        return {
            "status": "ok",
            "v": "5"
        }


class ByNameResource(Resource):
    def get(self, name):
        data = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        raw = data.json()
        abilities_full = raw["abilities"]
        abilities = []
        for x in abilities_full:
            abilities.append(x["ability"]["name"])
        return {
            "name": name,
            "weight": raw["weight"],
            "height": raw["height"],
            "abilities": abilities,
        }


api.add_resource(HealthResource, '/health')
api.add_resource(ByNameResource, '/api/by-name/<name>')


# https://pokeapi.co/api/v2/pokemon/ditto
# al API que ya tenemos agregale, el campo stats
# stats: {
#   hp:48,
#   attack:48,
#   defense:48,
#   ...
# }