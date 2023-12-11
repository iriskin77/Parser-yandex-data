from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_sqlite(self):
        abs_path: Path = Path(__file__).resolve().parent.parent
        sqlite_db_path = f'sqlite:////{abs_path}/Parser/sqlite.db'
        return sqlite_db_path

settings = Settings()