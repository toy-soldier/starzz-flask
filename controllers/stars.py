"""This module defines the functions called when the Star* resources are invoked."""
from __future__ import annotations

from http import HTTPStatus
from flask_restful.reqparse import Namespace

from models import stars


def handle_post(data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    stars.Star.create(data)
    return {
        "message": "Star successfully registered."
    }, HTTPStatus.CREATED


def handle_get(star_id: int) -> tuple[dict[str, str | int |
                                                         dict[str, str | int]], int]:
    """Handle the GET request."""
    obj = stars.Star.retrieve(star_id)
    if not obj:
        return {
            "message": "Star not found."
        }, HTTPStatus.NOT_FOUND

    return {
        "result": obj,
        "message": "Star successfully retrieved."
    }, HTTPStatus.OK


def handle_put(star_id: int, data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    if not stars.Star.update(star_id, data):
        return {
            "message": "Star to update not found."
        }, HTTPStatus.BAD_REQUEST

    return {
        "message": "Star successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(star_id: int) -> tuple[dict[str, str] | None, int]:
    """Handle the DELETE request."""
    if not stars.Star.delete(star_id):
        return {
            "message": "Star to delete not found."
        }, HTTPStatus.BAD_REQUEST

    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str | int], int]:
    """Handle the GET request."""
    return {
        "result": stars.Star.list(),
        "message": "Stars successfully retrieved."
    }, HTTPStatus.OK
