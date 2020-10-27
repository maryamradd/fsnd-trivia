"""Api Blueprints."""

from flask import Blueprint
from flask_cors import CORS


api = Blueprint("app", __name__)
CORS(api, resources={r"/api/*": {"origins": "*"}})

from . import routes  # importing routes