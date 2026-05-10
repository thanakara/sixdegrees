from sixdegrees.app.extensions import get_session
from sixdegrees.app.blueprints.main.queries import resolve_person_name


def path_graph(name_a: str, name_b: str) -> dict | None:
    """
    Returns shortest path between two people as vis-network nodes/edges.
    """

    resolved_a = resolve_person_name(name_a)
    resolved_b = resolve_person_name(name_b)

    if not resolved_a or not resolved_b:
        return None

    cypher = """
    MATCH (a:Person {name: $name_a}),
          (b:Person {name: $name_b})
    MATCH path = shortestPath((a)-[:ACTED_IN|DIRECTED*..10]-(b))
    RETURN nodes(path) AS nodes, relationships(path) AS rels
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

    nodes = []
    edges = []
    seen_nodes = set()

    for node in record["nodes"]:
        node_id = node.element_id
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)

        if "Person" in node.labels:
            nodes.append(
                {
                    "id": node_id,
                    "label": node["name"],
                    "group": "person",
                    "title": f"b. {node['birthYear']}" if node["birthYear"] else "",
                }
            )
        elif "Movie" in node.labels:
            nodes.append(
                {
                    "id": node_id,
                    "label": node["title"],
                    "group": "movie",
                    "title": f"{node['year']} · ★ {node['averageRating']}",
                }
            )

    for rel in record["rels"]:
        edges.append(
            {
                "from": rel.start_node.element_id,
                "to": rel.end_node.element_id,
                "label": rel.type.replace("_", " "),
                "dashes": rel.type == "DIRECTED",
            }
        )

    return {"nodes": nodes, "edges": edges}


def person_graph(person_id: str) -> dict | None:
    cypher = """
    MATCH (p:Person {person_id: $person_id})-[r:ACTED_IN|DIRECTED]->(m:Movie)
    RETURN p, collect({movie: m, rel: r}) AS films
    """

    with get_session() as session:
        record = session.run(cypher, parameters={"person_id": person_id}).single()

    if record is None:
        return None

    nodes = []
    edges = []
    seen_nodes = set()

    p = record["p"]
    p_id = p.element_id
    seen_nodes.add(p_id)
    nodes.append(
        {
            "id": p_id,
            "label": p["name"],
            "group": "person",
            "title": f"b. {p['birthYear']}" if p["birthYear"] else "",
        }
    )

    for film in record["films"]:
        m = film["movie"]
        rel = film["rel"]
        m_id = m.element_id

        if m_id not in seen_nodes:
            seen_nodes.add(m_id)
            nodes.append(
                {
                    "id": m_id,
                    "label": m["title"],
                    "group": "movie",
                    "title": f"{m['year']} · ★ {m['averageRating']}",
                    "movie_id": m["movie_id"],
                }
            )

        edges.append(
            {
                "from": p_id,
                "to": m_id,
                "label": rel.type.replace("_", " "),
                "dashes": rel.type == "DIRECTED",
            }
        )

    return {"nodes": nodes, "edges": edges}


def expand_movie(movie_id: str) -> dict | None:
    """
    Returns cast of a movie as vis-network nodes/edges.
    Used for click-to-expand on person page.
    """

    cypher = """
    MATCH (m:Movie {movie_id: $movie_id})<-[r:ACTED_IN|DIRECTED]-(p:Person)
    RETURN m, collect({person: p, rel: r}) AS cast
    """

    with get_session() as session:
        record = session.run(cypher, parameters={"movie_id": movie_id}).single()

    if record is None:
        return None

    nodes = []
    edges = []

    m = record["m"]
    nodes.append(
        {
            "id": m.element_id,
            "label": m["title"],
            "group": "movie",
            "title": f"{m['year']} · ★ {m['averageRating']}",
            "movie_id": m["movie_id"],
        }
    )

    for member in record["cast"]:
        p = member["person"]
        rel = member["rel"]
        nodes.append(
            {
                "id": p.element_id,
                "label": p["name"],
                "group": "person",
                "title": f"b. {p['birthYear']}" if p["birthYear"] else "",
            }
        )
        edges.append(
            {
                "from": p.element_id,
                "to": m.element_id,
                "label": rel.type.replace("_", " "),
                "dashes": rel.type == "DIRECTED",
            }
        )

    return {"nodes": nodes, "edges": edges}
