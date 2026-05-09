from flask import abort, render_template

from sixdegrees.app.blueprints.genre import bp
from sixdegrees.app.blueprints.genre.queries import get_genre


@bp.get("/<name>")
def detail(name: str):
    genre = get_genre(name)

    if genre is None:
        abort(404)

    return render_template("genre/detail.html", genre=genre)
