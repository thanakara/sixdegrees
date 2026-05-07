from functools import lru_cache

from neo4j import GraphDatabase

from sixdegrees.config import settings


@lru_cache
def get_driver():
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=settings.neo4j_auth,
    )


def get_session():
    driver = get_driver()
    return driver.session()
