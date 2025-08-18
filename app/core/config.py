from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    # API_V1_STR: str = "/api/v1"
    # JWT_SECRET: str = os.getenv("JWT_SECRET")
    # JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRES: str
    API_V1_STR: str = "/api/v1"

    # class Config:
    #     env_file = ".env"
    #     extra = "ignore"  # option temporaire pour accepter un .env qui contient des variables non utilisées ici.


settings = Settings()
