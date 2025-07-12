"""This module defines the Galaxy model for the CRUD operations."""
from __future__ import annotations

from typing_extensions import Self

from sqlalchemy.orm import relationship

from config import db
from models.users import User


class Galaxy(db.Model):
    """Model for Galaxy objects."""
    __tablename__ = "galaxies"

    galaxy_id = db.Column(db.Integer, primary_key=True)
    galaxy_name = db.Column(db.String)
    galaxy_type = db.Column(db.String)
    distance_mly = db.Column(db.Integer)
    redshift = db.Column(db.Integer)
    mass_solar = db.Column(db.Integer)
    diameter_ly = db.Column(db.Integer)
    added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    verified_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    galaxy_added_info = relationship("User", foreign_keys=[added_by])
    galaxy_verified_info = relationship("User", foreign_keys=[verified_by])

    def __init__(self, data: dict[str, str | int]) -> None:
        self.galaxy_id = data["galaxy_id"]
        self.galaxy_name = data["galaxy_name"]
        self.galaxy_type = data["galaxy_type"]
        self.distance_mly = data["distance_mly"]
        self.redshift = data["redshift"]
        self.mass_solar = data["mass_solar"]
        self.diameter_ly = data["diameter_ly"]
        self.added_by = data["added_by"]
        self.verified_by = data["verified_by"]

    @classmethod
    def search(cls, galaxy_id: int) -> Self | None:
        """Return the desired galaxy object."""
        return cls.query.get(galaxy_id)

    @classmethod
    def create(cls, data: dict[str, str | int]) -> None:
        """Insert a new object into the database."""
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def retrieve(cls, galaxy_id: int) -> dict[str, str | int] | None:
        """Return a JSON representation of the object if found, otherwise return None."""
        obj = cls.search(galaxy_id)
        if not obj:
            return None
        return obj.to_full_json()

    @classmethod
    def update(cls, galaxy_id: int, data: dict[str, str | int]) -> bool:
        """Update the object in the database."""
        obj = cls.search(galaxy_id)
        if not obj:
            return False

        data["galaxy_id"] = galaxy_id
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, galaxy_id: int) -> bool:
        """Delete the object from the database."""
        obj = cls.search(galaxy_id)
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
            "galaxy_id": self.galaxy_id,
            "galaxy_name": self.galaxy_name
        }

    def to_full_json(self) -> dict[str, str | int | dict[str, str | int]]:
        """Return a full JSON representation of this object."""
        obj = self.galaxy_added_info
        added_by = obj.to_partial_json() if obj else {}
        obj = self.galaxy_verified_info
        verified_by = obj.to_partial_json() if obj else {}

        return {
            **self.to_partial_json(),
            "galaxy_type": self.galaxy_type,
            "distance_mly": self.distance_mly,
            "redshift": self.redshift,
            "mass_solar": self.mass_solar,
            "diameter_ly": self.diameter_ly,
            "added_by": added_by,
            "verified_by": verified_by
        }
