from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
