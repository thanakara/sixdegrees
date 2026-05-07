from sixdegrees.app.extensions import get_session


def get_person(person_id: str) -> dict | None:
    """
    Fetch a person and their full filmography (acted + directed).
    Returns None if the person_id doesn't exist.
    """

    cypher = """
    MATCH (p:Person {person_id: $person_id})
    OPTIONAL MATCH (p)-[:ACTED_IN]->(acted:Movie)
    OPTIONAL MATCH (p)-[:DIRECTED]->(directed:Movie)
    RETURN
        p.person_id          AS id,
        p.name               AS name,
        p.birthYear          AS birthYear,
        p.primaryProfession  AS profession,
        collect(DISTINCT {
            id:     acted.movie_id,
            title:  acted.title,
            year:   acted.year,
            rating: acted.averageRating
        }) AS acted_in,
        collect(DISTINCT {
            id:     directed.movie_id,
            title:  directed.title,
            year:   directed.year,
            rating: directed.averageRating
        }) AS directed
    """

    with get_session() as session:
        record = session.run(cypher, person_id=person_id).single()

    if record is None:
        return None

    return dict(record)
