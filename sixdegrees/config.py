from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr

    flask_env: str = "development"
    debug: bool = True

    batch_size: int = 5_000

    @property
    def neo4j_auth(self):
        return (self.neo4j_user, self.neo4j_password.get_secret_value())


settings = Settings()
