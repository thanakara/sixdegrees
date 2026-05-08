from flask import jsonify, request, render_template

from sixdegrees.config import settings
from sixdegrees.app.blueprints.main import bp
from sixdegrees.app.blueprints.main.queries import search_people, shortest_path


@bp.get("/")
def index():
    return render_template("main/index.html")


@bp.get("/path")
def path():
    name_a = request.args.get("a", "").strip()
    name_b = request.args.get("b", "").strip()

    result = None
    error = None

    if name_a and name_b:
        result = shortest_path(name_a, name_b)
        if result is None:
            error = f"No path found between {name_a!r} and {name_b!r}."

    return render_template(
        "main/path.html",
        name_a=name_a,
        name_b=name_b,
        result=result,
        error=error,
        neo4j_uri=settings.neo4j_uri,
        neo4j_user=settings.neo4j_user,
        neo4j_password=settings.neo4j_password.get_secret_value(),
    )


@bp.get("/search")
def search():
    """Autocomplete endpoint — returns JSON, consumed by the search inputs."""

    query = request.args.get("q", "").strip()
    if len(query) < 2:  # noqa: PLR2004
        return jsonify([])
    return jsonify(search_people(query))
