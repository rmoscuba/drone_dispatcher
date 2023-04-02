"""Data models."""
import datetime
import uuid
import enum
from sqlalchemy import Enum

from app import db

class ModelEnum(enum.Enum):
    Lightweight = 1, 
    Middleweight = 2, 
    Cruiserweight = 3, 
    Heavyweight = 4
    
    def __html__(self):
        """
        Return the html representation of the enum value.
        """
        return self.name


class StateEnum(enum.Enum):
    IDLE = 1,
    LOADING = 2,
    LOADED = 3,
    DELIVERING = 4,
    DELIVERED = 5,
    RETURNING = 6

    def __html__(self):
        """
        Return the html representation of the enum value.
        """
        return self.name

# The Drone class is a data model for medications
class Drone(db.Model):
    """Data model for drones."""

    __tablename__ = "drones"
    id = db.Column(db.Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    serial_number = db.Column(db.String(100), index=True, unique=True, nullable=False)
    model = db.Column('model', Enum(ModelEnum))
    weight_limit = db.Column(db.Integer(), nullable=False)
    battery_capacity = db.Column(db.Integer(), nullable=False)
    state = db.Column('state', Enum(StateEnum))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)

    medications = db.relationship('Medication', backref='drone', lazy='dynamic')

    def __init__(self, **kwargs):
        """
        Init drone data from a dictionary
        """
        self.serial_number = kwargs.get("serial_number")
        self.model = kwargs.get("model")
        self.weight_limit = kwargs.get("weight_limit")
        self.battery_capacity = kwargs.get("battery_capacity")
        self.state = kwargs.get("state")

    def as_dict(self):
        """
        Return drone data as a dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """
        Return a readable representation of the drone.
        """
        return "<{}>".format(self.serial_number)

    def update(self, values):
        """
        Update drone data from a dictionary
        """
        for key, value in values.items():
            if hasattr(self, key):
                setattr(self, key, value)
