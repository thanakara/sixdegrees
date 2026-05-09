from sixdegrees.app.extensions import get_session


def get_genre(name: str) -> dict | None:
    """
    Fetch a genre and its top 50 movies by popularity.
    Resolves case by capitalising the first letter.
    Returns None if the genre doesn't exist.
    """

    cypher = """
    MATCH (g:Genre)
    WHERE toLower(g.genre) = toLower($name)
    MATCH (m:Movie)-[:HAS_GENRE]->(g)
    RETURN
        g.genre         AS genre,
        collect({
            id:     m.movie_id,
            title:  m.title,
            year:   m.year,
            rating: m.averageRating,
            votes:  m.numVotes
        })[0..50] AS movies
    """

    with get_session() as session:
        record = session.run(cypher, parameters={"name": name}).single()

    if record is None:
        return None

    return {
        "genre": record["genre"],
        "movies": sorted(
            [dict(m) for m in record["movies"]],
            key=lambda m: m["votes"] or 0,
            reverse=True,
        ),
    }


def get_all_genres() -> list[str]:
    """Fetch all genre names — used for the genre index if needed later."""

    cypher = "MATCH (g:Genre) RETURN g.genre AS genre ORDER BY g.genre"
    with get_session() as session:
        return [r["genre"] for r in session.run(cypher)]
