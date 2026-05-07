from flask import Blueprint

bp = Blueprint("movie", __name__, template_folder="templates")

from sixdegrees.app.blueprints.movie import routes  # noqa: E402, F401
