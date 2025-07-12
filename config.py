"""This module contains the configuration of the Flask application."""
import pathlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from deps import constants


basedir = pathlib.Path(__file__).parent.resolve()
app = Flask(__name__)

# specify the location of the database file
app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLITE_URI.format(basedir)
# turns the SQLAlchemy event system off
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
