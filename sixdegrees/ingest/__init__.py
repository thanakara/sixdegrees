from pathlib import Path

PROCESSED_PATH = Path(__file__).parents[2] / "data" / "processed"

MOVIES_CYPHER = """
UNWIND $rows AS row
MERGE (m:Movie {movie_id: row.movie_id})
SET
    m.title         = row.title,
    m.year          = toInteger(row.year),
    m.runtime       = toInteger(row.runtime),
    m.averageRating = toFloat(row.averageRating),
    m.numVotes      = toInteger(row.numVotes)
"""

PEOPLE_CYPHER = """
UNWIND $rows AS row
MERGE (p:Person {person_id: row.person_id})
SET
    p.name              = row.name,
    p.birthYear         = toInteger(row.birthYear),
    p.primaryProfession = row.primaryProfession
"""

GENRES_CYPHER = """
UNWIND $rows AS row
MERGE (:Genre {genre: row.genre})
"""

ACTED_IN_CYPHER = """
UNWIND $rows AS row
MATCH (p:Person {person_id: row.source})
MATCH (m:Movie  {movie_id:  row.target})
MERGE (p)-[:ACTED_IN]->(m)
"""

DIRECTED_CYPHER = """
UNWIND $rows AS row
MATCH (p:Person {person_id: row.source})
MATCH (m:Movie  {movie_id:  row.target})
MERGE (p)-[:DIRECTED]->(m)
"""

HAS_GENRE_CYPHER = """
UNWIND $rows AS row
MATCH (m:Movie {movie_id: row.source})
MATCH (g:Genre {genre:    row.target})
MERGE (m)-[:HAS_GENRE]->(g)
"""
