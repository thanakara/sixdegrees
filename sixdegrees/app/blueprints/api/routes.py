from flask import abort, jsonify, request

from sixdegrees.app.blueprints.api import bp
from sixdegrees.app.blueprints.api.queries import path_graph, expand_movie, person_graph


@bp.get("/path")
def path():
    name_a = request.args.get("a", "").strip()
    name_b = request.args.get("b", "").strip()

    if not name_a or not name_b:
        abort(422)

    result = path_graph(name_a, name_b)
    if result is None:
        return jsonify({"nodes": [], "edges": []}), 404

    return jsonify(result)


@bp.get("/person/<person_id>/graph")
def person(person_id: str):
    result = person_graph(person_id)
    if result is None:
        abort(404)
    return jsonify(result)


@bp.get("/movie/<movie_id>/expand")
def expand(movie_id: str):
    result = expand_movie(movie_id)
    if result is None:
        abort(404)
    return jsonify(result)
