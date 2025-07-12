"""This module defines the GalaxyRegisterOrList() and Galaxy() resources to handle requests to /user."""
from flask_restful import Resource, reqparse

from controllers import galaxies
from deps import constants


def parse_request() -> reqparse.Namespace:
    """Parse the user's request."""
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("galaxy_id",
                        type=int
                        )
    parser.add_argument("galaxy_name",
                        type=str,
                        required=True,
                        help=constants.VALIDATE_NOT_NULL
                        )
    parser.add_argument("galaxy_type",
                        type=str
                        )
    parser.add_argument("distance_mly",
                        type=int
                        )
    parser.add_argument("redshift",
                        type=int
                        )
    parser.add_argument("mass_solar",
                        type=int
                        )
    parser.add_argument("diameter_ly",
                        type=int
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


class GalaxyRegisterOrList(Resource):
    """Resource to handle requests to register new, or list the existing, galaxies."""

    def post(self) -> tuple[dict[str, str], int]:
        """Handle POST method."""
        data = parse_request()
        return galaxies.handle_post(data)

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
        data = parse_request()
        return galaxies.handle_put(galaxy_id, data)

    def delete(self, galaxy_id: int) -> tuple[None, int]:
        """Handle DELETE method."""
        return galaxies.handle_delete(galaxy_id)
