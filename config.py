from pydantic import BaseSettings, UUID4
from models.user import UserCreate

class Settings(BaseSettings):
    secret: str  # automatically taken from environment variable

class User(UserCreate):
    id: UUID4

DEFAULT_SETTINGS = Settings(_env_file=".env")
DB = {
    "users": {}
}

TOKEN_URL = "/auth/token"