"""Data models."""
import datetime
import uuid

from app import db


# The Medication class is a data model for medications
class Medication(db.Model):
    """Data model for medications."""

    __tablename__ = "medications"
    id = db.Column(db.Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    code = db.Column(db.String(64), index=True, unique=True, nullable=False)
    image = db.Column(db.String(256), nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    
    drone_id = db.Column(db.Text(length=36), db.ForeignKey('drones.id'))

    def __init__(self, **kwargs):
        """
        Init medication data from a dictionary
        """
        self.name = kwargs.get("name")
        self.weight = kwargs.get("weight")
        self.code = kwargs.get("code")
        self.image = kwargs.get("image")
        self.drone_id = kwargs.get("drone_id")

    def as_dict(self):
        """
        Return medication data as a dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """
        Return a readable respresantation of the medication.
        """
        return "<{}>".format(self.name)

    def update(self, values):
        """
        Update medication data from a dictionary
        """
        for key, value in values.items():
            if hasattr(self, key):
                setattr(self, key, value)
