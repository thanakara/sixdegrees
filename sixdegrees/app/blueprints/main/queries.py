from sixdegrees.app.extensions import get_session


def shortest_path(name_a: str, name_b: str) -> dict | None:
    """
    Find the shortest path between two people through shared movies.
    Returns a dict with the hop chain and degree count, or None if no path exists.
    """

    cypher = """
    MATCH (a:Person {name: $name_a}),
          (b:Person {name: $name_b})
    MATCH path = shortestPath((a)-[:ACTED_IN|DIRECTED*..10]-(b))
    WITH nodes(path) AS hops
    RETURN [n IN hops |
        CASE labels(n)[0]
            WHEN 'Person' THEN {
                type:      'person',
                id:        n.person_id,
                name:      n.name,
                birthYear: n.birthYear
            }
            WHEN 'Movie' THEN {
                type:    'movie',
                id:      n.movie_id,
                title:   n.title,
                year:    n.year,
                rating:  n.averageRating
            }
        END
    ] AS chain
    """

    with get_session() as session:
        record = session.run(
            cypher,
            parameters={
                "name_a": name_a,
                "name_b": name_b,
            },
        ).single()

    if record is None:
        return None

    chain = [dict(node) for node in record["chain"]]
    return {
        "chain": chain,
        "degrees": len([n for n in chain if n["type"] == "movie"]),
    }


def search_people(query: str, limit: int = 10) -> list[dict]:
    """
    Search people by partial name match.
    Used for the search autocomplete on the index page.
    """

    cypher = """
    MATCH (p:Person)
    WHERE p.name CONTAINS $query
    RETURN p.person_id AS id,
           p.name      AS name,
           p.birthYear AS birthYear
    ORDER BY p.name
    LIMIT $limit
    """

    with get_session() as session:
        result = session.run(
            cypher,
            parameters={
                "query": query,
                "limit": limit,
            },
        )
        return [dict(r) for r in result]
