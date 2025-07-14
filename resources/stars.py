"""This module defines the StarRegisterOrList() and Star() resources to handle requests to /user."""
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from controllers import stars
from deps import constants


def parse_request() -> reqparse.Namespace:
    """Parse the user's request."""
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("star_id",
                        type=int
                        )
    parser.add_argument("star_name",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("star_type",
                        type=str
                        )
    parser.add_argument("constellation_id",
                        type=int,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("right_ascension",
                        type=int
                        )
    parser.add_argument("declination",
                        type=int
                        )
    parser.add_argument("apparent_magnitude",
                        type=int
                        )
    parser.add_argument("spectral_type",
                        type=str
                        )
    parser.add_argument("added_by",
                        type=int,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("verified_by",
                        type=int
                        )
    return parser.parse_args()


class StarRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, stars."""

    @jwt_required()
    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        data = parse_request()
        return stars.handle_post(data)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return stars.handle_list()


class Star(Resource):
    """Resource to handle requests to view, update and delete existing stars."""

    def get(self, star_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return stars.handle_get(star_id)

    @jwt_required()
    def put(self, star_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        data = parse_request()
        return stars.handle_put(star_id, data)

    @jwt_required()
    def delete(self, star_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return stars.handle_delete(star_id)
