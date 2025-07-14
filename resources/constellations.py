"""This module defines the ConstellationRegisterOrList() and Constellation() resources to handle requests to /user."""
from __future__ import annotations

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from controllers import constellations
from deps import constants


def parse_request() -> reqparse.Namespace:
    """Parse the user's request."""
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("constellation_id",
                        type=int
                        )
    parser.add_argument("constellation_name",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("galaxy_id",
                        type=int,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
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


class ConstellationRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, constellations."""

    @jwt_required()
    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        data = parse_request()
        return constellations.handle_post(data)

    def get(self) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return constellations.handle_list()


class Constellation(Resource):
    """Resource to handle requests to view, update and delete existing constellations."""

    def get(self, constellation_id: int) -> tuple[dict[str, str], int]:
        """Handle GET method."""
        return constellations.handle_get(constellation_id)

    @jwt_required()
    def put(self, constellation_id: int) -> tuple[dict[str, str], int]:
        """Handle PUT method."""
        data = parse_request()
        return constellations.handle_put(constellation_id, data)

    @jwt_required()
    def delete(self, constellation_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return constellations.handle_delete(constellation_id)
