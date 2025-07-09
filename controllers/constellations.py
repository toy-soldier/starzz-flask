"""This module defines the functions called when the Constellation* resources are invoked."""
from http import HTTPStatus


def handle_post(r_json: dict[str, str]) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    return {
        "input": r_json,
        "message": "Constellation successfully registered."
    }, HTTPStatus.CREATED


def handle_get(constellation_id: int) -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": constellation_id,
        "message": "Constellation successfully retrieved."
    }, HTTPStatus.OK


def handle_put(constellation_id: int) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    return {
        "input": constellation_id,
        "message": "Constellation successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(constellation_id: int) -> tuple[None, int]:
    """Handle the DELETE request."""
    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": "ALL",
        "message": "Constellations successfully retrieved."
    }, HTTPStatus.OK
