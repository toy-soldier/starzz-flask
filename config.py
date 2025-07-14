"""This module contains the configuration of the Flask application."""
import pathlib
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from deps import constants


basedir = pathlib.Path(__file__).parent.resolve()
app = Flask(__name__)

# specify the location of the database file
app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLITE_URI.format(basedir)
# turns the SQLAlchemy event system off
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# specify the JWT secret key and token expiration (in minutes)
app.config["JWT_SECRET_KEY"] = constants.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRES)

db = SQLAlchemy(app)
jwt = JWTManager(app)
