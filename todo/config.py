from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str  # automatically taken from environment variable

DEFAULT_SETTINGS = Settings(_env_file=".env")
TOKEN_URL = "/token"