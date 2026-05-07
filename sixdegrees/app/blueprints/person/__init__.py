from flask import Blueprint

bp = Blueprint("person", __name__, template_folder="templates")

from sixdegrees.app.blueprints.person import routes  # noqa: E402, F401
