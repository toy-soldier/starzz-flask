"""This is the dependencies module of our application."""
from flask_restful import Api

import config
from resources import constellations, galaxies, stars, users

def main() -> None:
    """The application entrypoint."""

    api = Api(config.app)

    api.add_resource(constellations.ConstellationRegisterOrList, "/constellations")
    api.add_resource(constellations.Constellation, "/constellations/<int:constellation_id>")
    api.add_resource(galaxies.GalaxyRegisterOrList, "/galaxies")
    api.add_resource(galaxies.Galaxy, "/galaxies/<int:galaxy_id>")
    api.add_resource(stars.StarRegisterOrList, "/stars")
    api.add_resource(stars.Star, "/stars/<int:star_id>")
    api.add_resource(users.UserRegisterOrList, "/users")
    api.add_resource(users.User, "/users/<int:user_id>")
    api.add_resource(users.UserLogin, "/login")

    config.app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
