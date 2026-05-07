from flask import abort, render_template

from sixdegrees.app.blueprints.movie import bp
from sixdegrees.app.blueprints.movie.queries import get_movie


@bp.get("/<movie_id>")
def detail(movie_id: str):
    movie = get_movie(movie_id)
    if movie is None:
        abort(404)
    return render_template("movie/detail.html", movie=movie)
