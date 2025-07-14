"""This module defines the functions called when the User* resources are invoked."""
from __future__ import annotations

from http import HTTPStatus
from flask_restful.reqparse import Namespace
from flask_jwt_extended import create_access_token

from controllers import hashing
from models import users


def handle_post(data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    plaintext_password = data.get("password")
    if plaintext_password:
        data["password"] = hashing.bcrypt(plaintext_password)
    users.User.create(data)
    return {
        "message": "User successfully registered."
    }, HTTPStatus.CREATED


def handle_get(user_id: int) -> tuple[dict[str, str | int |
                                                         dict[str, str | int]], int]:
    """Handle the GET request."""
    obj = users.User.retrieve(user_id)
    if not obj:
        return {
            "message": "User not found."
        }, HTTPStatus.NOT_FOUND

    return {
        "result": obj,
        "message": "User successfully retrieved."
    }, HTTPStatus.OK


def handle_put(user_id: int, data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the PUT request."""
    plaintext_password = data.get("password")
    if plaintext_password:
        data["password"] = hashing.bcrypt(plaintext_password)

    if not users.User.update(user_id, data):
        return {
            "message": "User to update not found."
        }, HTTPStatus.BAD_REQUEST

    return {
        "message": "User successfully updated."
    }, HTTPStatus.ACCEPTED


def handle_delete(user_id: int) -> tuple[dict[str, str] | None, int]:
    """Handle the DELETE request."""
    if not users.User.delete(user_id):
        return {
            "message": "User to delete not found."
        }, HTTPStatus.BAD_REQUEST

    return None, HTTPStatus.NO_CONTENT


def handle_list() -> tuple[dict[str, str | int], int]:
    """Handle the GET request."""
    return {
        "result": users.User.list(),
        "message": "Users successfully retrieved."
    }, HTTPStatus.OK


def handle_login(data: Namespace) -> tuple[dict[str, str], int]:
    """Handle the POST request."""
    username = data["username"]
    plaintext_password = data["password"]

    obj = users.User.search_by_username(username)
    if obj and hashing.verify(obj.password, plaintext_password):
        token = create_access_token(identity=username)
        return {
            "message": f"Logged in as {username}.",
            "token": token
        }, HTTPStatus.OK

    return {
        "message": "Invalid credentials."
    }, HTTPStatus.UNAUTHORIZED
