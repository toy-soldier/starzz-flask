"""This is the main module of our application."""
from flask import Flask
from flask_restful import Api
from resources import constellations, galaxies, stars, users


app = Flask(__name__)
api = Api(app)

api.add_resource(constellations.ConstellationRegisterOrList, "/constellations")
api.add_resource(constellations.Constellation, "/constellations/<int:constellation_id>")
api.add_resource(galaxies.GalaxyRegisterOrList, "/galaxies")
api.add_resource(galaxies.Galaxy, "/galaxies/<int:galaxy_id>")
api.add_resource(stars.StarRegisterOrList, "/stars")
api.add_resource(stars.Star, "/stars/<int:star_id>")
api.add_resource(users.UserRegisterOrList, "/users")
api.add_resource(users.User, "/users/<int:user_id>")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
