"""This module defines the Constellation model for the CRUD operations."""
from __future__ import annotations

from typing_extensions import Self

from sqlalchemy.orm import relationship

from config import db
from models.galaxies import Galaxy
from models.users import User


class Constellation(db.Model):
    """Model for Constellation objects."""
    __tablename__ = "constellations"

    constellation_id = db.Column(db.Integer, primary_key=True)
    constellation_name = db.Column(db.String)
    galaxy_id = db.Column(db.Integer, db.ForeignKey("galaxies.galaxy_id"))
    added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    verified_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    galaxy_info = relationship("Galaxy")
    constellation_added_info = relationship("User", foreign_keys=[added_by])
    constellation_verified_info = relationship("User", foreign_keys=[verified_by])

    def __init__(self, data: dict[str, str | int]) -> None:
        self.constellation_id = data["constellation_id"]
        self.constellation_name = data["constellation_name"]
        self.galaxy_id = data["galaxy_id"]
        self.added_by = data["added_by"]
        self.verified_by = data["verified_by"]

    @classmethod
    def search(cls, constellation_id: int) -> Self | None:
        """Return the desired constellation object."""
        return cls.query.get(constellation_id)

    @classmethod
    def create(cls, data: dict[str, str | int]) -> None:
        """Insert a new object into the database."""
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def retrieve(cls, constellation_id: int) -> dict[str, str | int] | None:
        """Return a JSON representation of the object if found, otherwise return None."""
        obj = cls.search(constellation_id)
        if not obj:
            return None
        return obj.to_full_json()

    @classmethod
    def update(cls, constellation_id: int, data: dict[str, str | int]) -> bool:
        """Update the object in the database."""
        obj = cls.search(constellation_id)
        if not obj:
            return False

        data["constellation_id"] = constellation_id
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.add(obj)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, constellation_id: int) -> bool:
        """Delete the object from the database."""
        obj = cls.search(constellation_id)
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
            "constellation_id": self.constellation_id,
            "constellation_name": self.constellation_name
        }

    def to_full_json(self) -> dict[str, str | int | dict[str, str | int]]:
        """Return a full JSON representation of this object."""
        obj = self.galaxy_info
        galaxy = obj.to_partial_json() if obj else {}
        obj = self.constellation_added_info
        added_by = obj.to_partial_json() if obj else {}
        obj = self.constellation_verified_info
        verified_by = obj.to_partial_json() if obj else {}

        return {
            **self.to_partial_json(),
            "galaxy": galaxy,
            "added_by": added_by,
            "verified_by": verified_by
        }
