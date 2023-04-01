"""Data models."""
import datetime
import uuid

from sqlalchemy import UUID
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db


# The User class is a data model for user accounts
class User(db.Model):
    """Data model for users."""

    __tablename__ = "users"
    id = db.Column(db.Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)

    def __init__(self, **kwargs):
        """
        Init user data from a dictionary
        """
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def __repr__(self):
        """
        Return a readable respresantation of the user.
        """
        return "<User {}>".format(self.username)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        """
        :param password: The password to checked
        :return True if the password match
        """
        return check_password_hash(self.password, password)