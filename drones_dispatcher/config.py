"""Flask configuration variables."""
from os import environ, path
import os

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")

    # File upload
    UPLOAD_FOLDER = os.path.abspath(environ.get("UPLOAD_FOLDER"))
    MAX_CONTENT_LENGTH = int(environ.get("MAX_CONTENT_LENGTH"))

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False