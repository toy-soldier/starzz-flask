"""This module defines the UserRegister() and User() resources to handle requests to /user."""
from flask import request
from flask_restful import Resource

from controllers import users


class UserRegisterOrList(Resource):
    """Resource to handle requests to register new, or list existing, users."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        return users.handle_post(request.json)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return users.handle_list()


class User(Resource):
    """Resource to handle requests to view, update and delete existing users."""

    def get(self, user_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return users.handle_get(user_id)

    def put(self, user_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        return users.handle_put(user_id)

    def delete(self, user_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return users.handle_delete(user_id)
