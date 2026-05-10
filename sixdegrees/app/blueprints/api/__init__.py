from flask import Blueprint

bp = Blueprint("api", __name__)

from sixdegrees.app.blueprints.api import routes  # noqa: E402, F401
