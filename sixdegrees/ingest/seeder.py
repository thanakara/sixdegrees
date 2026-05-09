from sixdegrees import log
from sixdegrees.ingest import (
    GENRES_CYPHER,
    MOVIES_CYPHER,
    PEOPLE_CYPHER,
    ACTED_IN_CYPHER,
    DIRECTED_CYPHER,
    HAS_GENRE_CYPHER,
)
from sixdegrees.app.extensions import get_session
from sixdegrees.ingest.helpers import load, read


def load_movies() -> None:
    load("nodes.Movie", MOVIES_CYPHER, read("nodes.Movie.csv"))


def load_people() -> None:
    load("nodes.Person", PEOPLE_CYPHER, read("nodes.Person.csv"))


def load_genres() -> None:
    load("nodes.Genre", GENRES_CYPHER, read("nodes.Genre.csv"))


def load_acted_in() -> None:
    load("edges.ACTED_IN", ACTED_IN_CYPHER, read("edges.ACTED_IN.csv"))


def load_directed() -> None:
    load("edges.DIRECTED", DIRECTED_CYPHER, read("edges.DIRECTED.csv"))


def load_has_genre() -> None:
    load("edges.HAS_GENRE", HAS_GENRE_CYPHER, read("edges.HAS_GENRE.csv"))


def verify() -> None:
    cypher = """
    MATCH (n)
    RETURN labels(n)[0] AS label, count(*) AS total
    UNION ALL
    MATCH ()-[r]->()
    RETURN type(r) AS label, count(*) AS total
    ORDER BY total DESC
    """
    log.info("=== Verification ===")
    with get_session() as session:
        for row in session.run(cypher):
            log.info(f"  {row['label']:<20} {row['total']:>10,}")


def main() -> None:
    # check: idempotent
    with get_session() as session:
        count = session.run("MATCH (m:Movie) RETURN count(m) AS n").single()["n"]
        if count > 0:
            log.info("Database already seeded — skipping.")
            return

    load_movies()
    load_people()
    load_genres()

    load_acted_in()
    load_directed()
    load_has_genre()

    verify()


if __name__ == "__main__":
    main()
