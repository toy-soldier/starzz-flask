"""This module defines the GalaxyRegisterOrList() and Galaxy() resources to handle requests to /user."""
from flask import request
from flask_restful import Resource

from controllers import galaxies


class GalaxyRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, galaxies."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        return galaxies.handle_post(request.json)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return galaxies.handle_list()


class Galaxy(Resource):
    """Resource to handle requests to view, update and delete existing galaxies."""

    def get(self, galaxy_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return galaxies.handle_get(galaxy_id)

    def put(self, galaxy_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        return galaxies.handle_put(galaxy_id)

    def delete(self, galaxy_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return galaxies.handle_delete(galaxy_id)
