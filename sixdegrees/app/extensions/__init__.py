from flask import Flask
from neo4j import GraphDatabase  # noqa: F401


class Neo4jDatabase:
    def __init__(self):
        self.driver = None

    def init_app(self, app: Flask): ...
