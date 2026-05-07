from sixdegrees.app.extensions import get_session


def get_movie(movie_id: str) -> dict | None:
    """
    Fetch a movie and its full cast/director list.
    Returns None if the movie_id doesn't exist.
    """

    cypher = """
    MATCH (m:Movie {movie_id: $movie_id})
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(actor:Person)
    OPTIONAL MATCH (m)<-[:DIRECTED]-(director:Person)
    OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
    RETURN
        m.movie_id      AS id,
        m.title         AS title,
        m.year          AS year,
        m.runtime       AS runtime,
        m.averageRating AS rating,
        m.numVotes      AS numVotes,
        collect(DISTINCT {id: actor.person_id,   name: actor.name})    AS cast,
        collect(DISTINCT {id: director.person_id, name: director.name}) AS directors,
        collect(DISTINCT g.genre) AS genres
    """

    with get_session() as session:
        record = session.run(cypher, movie_id=movie_id).single()

    if record is None:
        return None

    return dict(record)
