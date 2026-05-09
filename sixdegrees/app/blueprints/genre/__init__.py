from flask import Blueprint

bp = Blueprint("genre", __name__, template_folder="templates")

from sixdegrees.app.blueprints.genre import routes  # noqa: E402, F401
