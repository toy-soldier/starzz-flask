"""This module defines the functions called when the Galaxy* resources are invoked."""
from __future__ import annotations

from http import HTTPStatus
from flask_restful.reqparse import Namespace

from models import galaxies


def handle_post(data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    galaxies.Galaxy.create(data)
    return {
        "message": "Galaxy successfully registered."
    }, HTTPStatus.CREATED


def handle_get(galaxy_id: int) -> tuple[dict[str, str | int |
                                                         dict[str, str | int]], int]:
    """Handle the GET request."""
    obj = galaxies.Galaxy.retrieve(galaxy_id)
    if not obj:
        return {
            "message": "Galaxy not found."
        }, HTTPStatus.NOT_FOUND

    return {
        "result": obj,
        "message": "Galaxy successfully retrieved."
    }, HTTPStatus.OK


def handle_put(galaxy_id: int, data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    if not galaxies.Galaxy.update(galaxy_id, data):
        return {
            "message": "Galaxy to update not found."
        }, HTTPStatus.BAD_REQUEST

    return {
        "message": "Galaxy successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(galaxy_id: int) -> tuple[dict[str, str] | None, int]:
    """Handle the DELETE request."""
    if not galaxies.Galaxy.delete(galaxy_id):
        return {
            "message": "Galaxy to delete not found."
        }, HTTPStatus.BAD_REQUEST

    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str | int], int]:
    """Handle the GET request."""
    return {
        "result": galaxies.Galaxy.list(),
        "message": "Galaxies successfully retrieved."
    }, HTTPStatus.OK
