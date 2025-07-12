"""This module defines the functions called when the Constellation* resources are invoked."""
from __future__ import annotations

from http import HTTPStatus
from flask_restful.reqparse import Namespace

from models import constellations


def handle_post(data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    constellations.Constellation.create(data)
    return {
        "message": "Constellation successfully registered."
    }, HTTPStatus.CREATED


def handle_get(constellation_id: int) -> tuple[dict[str, str | int |
                                                         dict[str, str | int]], int]:
    """Handle the GET request."""
    obj = constellations.Constellation.retrieve(constellation_id)
    if not obj:
        return {
            "message": "Constellation not found."
        }, HTTPStatus.NOT_FOUND

    return {
        "result": obj,
        "message": "Constellation successfully retrieved."
    }, HTTPStatus.OK


def handle_put(constellation_id: int, data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    if not constellations.Constellation.update(constellation_id, data):
        return {
            "message": "Constellation to update not found."
        }, HTTPStatus.BAD_REQUEST

    return {
        "message": "Constellation successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(constellation_id: int) -> tuple[dict[str, str] | None, int]:
    """Handle the DELETE request."""
    if not constellations.Constellation.delete(constellation_id):
        return {
            "message": "Constellation to delete not found."
        }, HTTPStatus.BAD_REQUEST

    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str | int], int]:
    """Handle the GET request."""
    return {
        "result": constellations.Constellation.list(),
        "message": "Constellations successfully retrieved."
    }, HTTPStatus.OK
