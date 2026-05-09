from sixdegrees.app.extensions import get_session


def resolve_person_name(name: str) -> str | None:
    """Resolve a case-insensitive name to the exact stored name."""

    cypher = """
    CALL db.index.fulltext.queryNodes('person_name_ft', $name)
    YIELD node, score
    RETURN node.name AS name
    ORDER BY score DESC
    LIMIT 1
    """

    with get_session() as session:
        record = session.run(cypher, parameters={"name": name}).single()

    return record["name"] if record else None


def shortest_path(name_a: str, name_b: str) -> dict | None:
    """
    Find the shortest path between two people through shared movies.
    Resolves names case-insensitively before querying.
    Returns a dict with the hop chain and degree count, or None if no path exists.
    """
    resolved_a = resolve_person_name(name_a)
    resolved_b = resolve_person_name(name_b)

    if not resolved_a or not resolved_b:
        return None

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
                type:   'movie',
                id:     n.movie_id,
                title:  n.title,
                year:   n.year,
                rating: n.averageRating
            }
        END
    ] AS chain
    """

    with get_session() as session:
        record = session.run(
            cypher,
            parameters={
                "name_a": resolved_a,
                "name_b": resolved_b,
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
    Case-insensitive, relevance ranked.
    """

    query = query.replace("+", "\\+").replace("-", "\\-")  # HACK
    cypher = """
    CALL db.index.fulltext.queryNodes('person_name_ft', $query)
    YIELD node, score
    RETURN
        node.person_id  AS id,
        node.name       AS name,
        node.birthYear  AS birthYear
    ORDER BY score DESC
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
