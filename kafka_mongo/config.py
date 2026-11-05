from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # MongoDB Atlas
    mongodb_uri: str
    mongodb_db: str = "final2026"

    # kafka / Confluent


def get_settings() -> Settings:

    return Settings()
