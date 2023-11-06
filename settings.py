from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bookssaving app"

    DATABASE_URL: str = "sqlite+aiosqlite:///./books.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
