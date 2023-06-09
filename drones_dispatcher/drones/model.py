"""Data models."""
import datetime
import uuid
import enum
from sqlalchemy import Enum
from sqlalchemy.orm import validates

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

    def next(self):
        """
        Return the consecutive Enum value
        """
        next_value = self.value[0]
        if next_value > 6:
            raise ValueError('No more values')
        return StateEnum(list(StateEnum)[next_value])


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

    def cannot_load_error(self, weight):
        """
        Return error message if drone cannot load a weight
        """
        if self.state != StateEnum.LOADING:
            return "Drone is not available for loading"
        load = self.weight_limit
        for medication in self.medications:
            load -= medication.weight
        if load < weight:
            return "Drone capacity reached"
        return None

    @validates("state")
    def validates_state(self, key, value):
        """
        Prevent the drone from being in LOADING state if the battery level is below 25%
        """
        if value == "LOADING" and self.battery_capacity < 25:
            raise ValueError("Drone can not be in LOADING state if the battery level is below 25%")
        return value
