"""This module defines the functions called when the User* resources are invoked."""
from http import HTTPStatus


def handle_post(r_json: dict[str, str]) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    return {
        "input": r_json,
        "message": "User successfully registered."
    }, HTTPStatus.CREATED


def handle_get(user_id: int) -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": user_id,
        "message": "User successfully retrieved."
    }, HTTPStatus.OK


def handle_put(user_id: int) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    return {
        "input": user_id,
        "message": "User successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(user_id: int) -> tuple[None, int]:
    """Handle the DELETE request."""
    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str], int]:
    """Handle the GET request."""
    return {
        "input": "ALL",
        "message": "Users successfully retrieved."
    }, HTTPStatus.OK
