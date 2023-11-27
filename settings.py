from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bookssaving app"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/books"

    UPLOADED_FILES_PATH = "uploads/"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
