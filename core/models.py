import sqlalchemy as sa
from core.database import Base
import typing as t


class Postcode(Base):
    __tablename__ = "postcode"
    id = sa.Column(sa.Integer, primary_key=True)
    postcode = sa.Column(sa.String(8), unique=True, index=True)
    latitude = sa.Column(sa.Float(6))
    longitude = sa.Column(sa.Float(6))
    users = sa.orm.relationship("User", back_populates="postcode")

    def __init__(self, postcode: str, latitude: float, longitude: float):
        self.postcode = postcode
        self.latitude = round(latitude, 6)
        self.longitude = round(longitude, 6)

    def __repr__(self):
        return "<Postcode %s:  %f %f>" % (self.postcode, self.latitude, self.longitude)


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    postcode_id = sa.Column(sa.Integer, sa.ForeignKey("postcode.id"))
    postcode = sa.orm.relationship("Postcode")
    email = sa.Column(sa.String(120), unique=True, nullable=False, index=True)
    status = sa.Column(sa.Boolean(), default=True)

    def __init__(self, email: str, status: bool = True, postcode: t.Any = None):
        self.postcode = postcode
        self.email = email
        self.status = status

    def __repr__(self):
        return "<User %r>" % (self.email)
