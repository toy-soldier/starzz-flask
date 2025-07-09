"""This module defines the StarRegisterOrList() and Star() resources to handle requests to /user."""
from flask import request
from flask_restful import Resource

from controllers import stars


class StarRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, stars."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        return stars.handle_post(request.json)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return stars.handle_list()


class Star(Resource):
    """Resource to handle requests to view, update and delete existing stars."""

    def get(self, star_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return stars.handle_get(star_id)

    def put(self, star_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        return stars.handle_put(star_id)

    def delete(self, star_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return stars.handle_delete(star_id)
