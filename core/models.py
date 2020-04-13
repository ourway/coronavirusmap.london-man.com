import sqlalchemy as sa
from core.database import Base
from uuid import uuid4
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
    token = sa.Column(sa.String, default=uuid4().hex, index=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False, index=True)
    status = sa.Column(sa.Boolean(), default=False)

    def __init__(
        self,
        email: str,
        postcode: t.Any = None,
        status: bool = False,
        token: str = uuid4().hex,
    ):
        self.postcode = postcode
        self.email = email
        self.status = status
        self.token = token

    def __repr__(self):
        return "<User %r>" % (self.email)
