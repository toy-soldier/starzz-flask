"""This module defines the UserRegister() and User() resources to handle requests to /user."""
from flask_restful import Resource, reqparse

from controllers import users
from deps import constants


def parse_request() -> reqparse.Namespace:
    """Parse the user's request."""
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("user_id",
                        type=int
                        )
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("email",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("first_name",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("last_name",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("date_of_birth",
                        type=str
                        )
    return parser.parse_args()


class UserRegisterOrList(Resource):
    """Resource to handle requests to register new, or list existing, users."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        data = parse_request()
        return users.handle_post(data)

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
        data = parse_request()
        return users.handle_put(user_id, data)

    def delete(self, user_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return users.handle_delete(user_id)
