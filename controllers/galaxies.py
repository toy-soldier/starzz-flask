"""This module defines the functions called when the Galaxy* resources are invoked."""
from http import HTTPStatus


def handle_post(r_json: dict[str, str]) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    return {
        "input": r_json,
        "message": "Galaxy successfully registered."
    }, HTTPStatus.CREATED


def handle_get(galaxy_id: int) -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": galaxy_id,
        "message": "Galaxy successfully retrieved."
    }, HTTPStatus.OK


def handle_put(galaxy_id: int) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    return {
        "input": galaxy_id,
        "message": "Galaxy successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(galaxy_id: int) -> tuple[None, int]:
    """Handle the DELETE request."""
    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": "ALL",
        "message": "Galaxies successfully retrieved."
    }, HTTPStatus.OK
