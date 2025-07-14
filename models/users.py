"""This module defines the User model for the CRUD operations."""
from __future__ import annotations

from typing_extensions import Self

from config import db



class User(db.Model):
    """Model for User objects."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.String)


    def __init__(self, data: dict[str, str | int]) -> None:
        self.user_id = data["user_id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.date_of_birth = data["date_of_birth"]

    @classmethod
    def search(cls, user_id: int) -> Self | None:
        """Return the desired user object."""
        return cls.query.get(user_id)

    @classmethod
    def search_by_username(cls, username: str) -> Self | None:
        """Return the desired user object."""
        return cls.query.filter(cls.username == username).first()

    @classmethod
    def create(cls, data: dict[str, str | int]) -> None:
        """Insert a new object into the database."""
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def retrieve(cls, user_id: int) -> dict[str, str | int] | None:
        """Return a JSON representation of the object if found, otherwise return None."""
        obj = cls.search(user_id)
        if not obj:
            return None
        return obj.to_full_json()

    @classmethod
    def update(cls, user_id: int, data: dict[str, str | int]) -> bool:
        """Update the object in the database."""
        obj = cls.search(user_id)
        if not obj:
            return False

        data["user_id"] = user_id
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, user_id: int) -> bool:
        """Delete the object from the database."""
        obj = cls.search(user_id)
        if not obj:
            return False

        db.session.delete(obj)
        db.session.commit()
        return True

    @classmethod
    def list(cls) -> list[dict[str, str | int]]:
        """Return a list of objects present in the database."""
        list_of_objs = cls.query.all()
        return [obj.to_partial_json() for obj in list_of_objs]

    def to_partial_json(self) -> dict[str, str | int]:
        """Return a partial JSON representation of this object."""
        return {
            "user_id": self.user_id,
            "full_name": f"{self.first_name} {self.last_name}"
        }

    def to_full_json(self) -> dict[str, str | int]:
        """Return a full JSON representation of this object."""
        return {
            **self.to_partial_json(),
            "username": self.username,
            "email": self.email,
            "date_of_birth": self.date_of_birth
        }
