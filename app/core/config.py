from typing import Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):

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
    #     extra = "ignore"  # option temporaire pour accepter
    #  un .env qui contient des variables non utilisées ici.


settings = Settings()
