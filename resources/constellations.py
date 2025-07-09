"""This module defines the ConstellationRegisterOrList() and Constellation() resources to handle requests to /user."""
from flask import request
from flask_restful import Resource

from controllers import constellations


class ConstellationRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, constellations."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        return constellations.handle_post(request.json)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return constellations.handle_list()


class Constellation(Resource):
    """Resource to handle requests to view, update and delete existing constellations."""

    def get(self, constellation_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return constellations.handle_get(constellation_id)

    def put(self, constellation_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        return constellations.handle_put(constellation_id)

    def delete(self, constellation_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return constellations.handle_delete(constellation_id)
