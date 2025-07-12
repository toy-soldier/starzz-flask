"""This module defines the Star model for the CRUD operations."""
from __future__ import annotations

from typing_extensions import Self

from sqlalchemy.orm import relationship

from config import db
from models.constellations import Constellation
from models.users import User


class Star(db.Model):
    """Model for Star objects."""
    __tablename__ = "stars"

    star_id = db.Column(db.Integer, primary_key=True)
    star_name = db.Column(db.String)
    star_type = db.Column(db.String)
    constellation_id = db.Column(db.Integer, db.ForeignKey("constellations.constellation_id"))
    right_ascension = db.Column(db.Integer)
    declination = db.Column(db.Integer)
    apparent_magnitude = db.Column(db.Integer)
    spectral_type = db.Column(db.String)
    added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    verified_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    constellation_info = relationship("Constellation")
    star_added_info = relationship("User", foreign_keys=[added_by])
    star_verified_info = relationship("User", foreign_keys=[verified_by])

    def __init__(self, data: dict[str, str | int]) -> None:
        self.star_id = data["star_id"]
        self.star_name = data["star_name"]
        self.star_type = data["star_type"]
        self.constellation_id = data["constellation_id"]
        self.right_ascension = data["right_ascension"]
        self.declination = data["declination"]
        self.apparent_magnitude = data["apparent_magnitude"]
        self.spectral_type = data["spectral_type"]
        self.added_by = data["added_by"]
        self.verified_by = data["verified_by"]

    @classmethod
    def search(cls, star_id: int) -> Self | None:
        """Return the desired star object."""
        return cls.query.get(star_id)

    @classmethod
    def create(cls, data: dict[str, str | int]) -> None:
        """Insert a new object into the database."""
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def retrieve(cls, star_id: int) -> dict[str, str | int] | None:
        """Return a JSON representation of the object if found, otherwise return None."""
        obj = cls.search(star_id)
        if not obj:
            return None
        return obj.to_full_json()

    @classmethod
    def update(cls, star_id: int, data: dict[str, str | int]) -> bool:
        """Update the object in the database."""
        obj = cls.search(star_id)
        if not obj:
            return False

        data["star_id"] = star_id
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, star_id: int) -> bool:
        """Delete the object from the database."""
        obj = cls.search(star_id)
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
            "star_id": self.star_id,
            "star_name": self.star_name
        }

    def to_full_json(self) -> dict[str, str | int | dict[str, str | int]]:
        """Return a full JSON representation of this object."""
        obj = self.constellation_info
        constellation = obj.to_partial_json() if obj else {}
        obj = self.star_added_info
        added_by = obj.to_partial_json() if obj else {}
        obj = self.star_verified_info
        verified_by = obj.to_partial_json() if obj else {}

        return {
            **self.to_partial_json(),
            "star_type": self.star_type,
            "constellation": constellation,
            "right_ascension": self.right_ascension,
            "declination": self.declination,
            "apparent_magnitude": self.apparent_magnitude,
            "spectral_type": self.spectral_type,
            "added_by": added_by,
            "verified_by": verified_by
        }
