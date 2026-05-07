from functools import lru_cache
from contextlib import contextmanager

from neo4j import GraphDatabase

from sixdegrees.config import settings


@lru_cache(maxsize=1)
def get_driver():
    """Singleton Driver. One per process, reused across requests"""

    return GraphDatabase.driver(
        uri=settings.neo4j_uri,
        auth=settings.neo4j_auth,
    )


@contextmanager
def get_session():
    """Context-managed session - always closes even on exception raise"""

    driver = get_driver()
    session = driver.session()
    try:
        yield session
    finally:
        session.close()


def close_driver():
    """On app teardown to flush the connection pool"""

    driver = get_driver()
    driver.close()
    get_driver.cache_clear()
