import pandas as pd

from neo4j import Session

from sixdegrees import log
from sixdegrees.ingest import PROCESSED_PATH
from sixdegrees.app.extensions import get_session


def load_movies(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MERGE (m:Movie {movie_id: row.movie_id})
    SET m.title = row.title,
        m.year = row.year,
        m.runtime = row.runtime,
        m.averageRating = row.averageRating,
        m.numVotes = row.numVotes
    """
    session.run(query, rows=df.to_dict("records"))


def load_people(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MERGE (p:Person {person_id: row.person_id})
    SET p.name = row.name,
        p.birthYear = row.birthYear,
        p.primaryProfession = row.primaryProfession
    """
    session.run(query, rows=df.to_dict("records"))


def load_genres(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MERGE (g:Genre {genre: row.genre})
    """
    session.run(query, rows=df.to_dict("records"))


def load_acted_in(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MATCH (p:Person {person_id: row.source})
    MATCH (m:Movie {movie_id: row.target})
    MERGE (p)-[r:ACTED_IN]->(m)
    SET r.characters = row.characters
    """
    session.run(query, rows=df.to_dict("records"))


def load_directed(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MATCH (p:Person {person_id: row.source})
    MATCH (m:Movie {movie_id: row.target})
    MERGE (p)-[:DIRECTED]->(m)
    """
    session.run(query, rows=df.to_dict("records"))


def load_has_genre(session: Session, df: pd.DataFrame):
    query = """
    UNWIND $rows AS row
    MATCH (m:Movie {movie_id: row.source})
    MATCH (g:Genre {genre: row.target})
    MERGE (m)-[:HAS_GENRE]->(g)
    """
    session.run(query, rows=df.to_dict("records"))


def main():
    movies = pd.read_csv(PROCESSED_PATH / "nodes.Movie.csv")
    people = pd.read_csv(PROCESSED_PATH / "nodes.Person.csv")
    genres = pd.read_csv(PROCESSED_PATH / "nodes.Genre.csv")

    acted_in = pd.read_csv(PROCESSED_PATH / "edges.ACTED_IN.csv")
    directed = pd.read_csv(PROCESSED_PATH / "edges.DIRECTED.csv")
    has_genre = pd.read_csv(PROCESSED_PATH / "edges.HAS_GENRE.csv")

    movies = movies.where(pd.notnull(movies), None)
    people = people.where(pd.notnull(people), None)
    genres = genres.where(pd.notnull(genres), None)

    with get_session() as session:
        log.info("LOAD CSV: nodes.Movie")
        load_movies(session, movies)

        log.info("LOAD CSV: nodes.Person")
        load_people(session, people)

        log.info("LOAD CSV: nodes.Genre")
        load_genres(session, genres)

        log.info("LOAD CSV: edges.ACTED_IN")
        load_acted_in(session, acted_in)

        log.info("LOAD CSV: edges.DIRECTED")
        load_directed(session, directed)

        log.info("LOAD CSV: edges.HAS_GENRE")
        load_has_genre(session, has_genre)


if __name__ == "__main__":
    main()
