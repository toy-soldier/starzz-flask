"""This module defines the functions called when the Star* resources are invoked."""
from http import HTTPStatus


def handle_post(r_json: dict[str, str]) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    return {
        "input": r_json,
        "message": "Star successfully registered."
    }, HTTPStatus.CREATED


def handle_get(star_id: int) -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": star_id,
        "message": "Star successfully retrieved."
    }, HTTPStatus.OK


def handle_put(star_id: int) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    return {
        "input": star_id,
        "message": "Star successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(star_id: int) -> tuple[None, int]:
    """Handle the DELETE request."""
    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": "ALL",
        "message": "Stars successfully retrieved."
    }, HTTPStatus.OK
