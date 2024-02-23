from pathlib import Path

from pydantic import BaseModel, PostgresDsn, model_validator
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class AppSettings(BaseSettings):
    class Config:
        env_prefix = "app_"

    root_path: str = ""
    debug: bool = True
    title: str = "Currency Exchanger"


class PostgresDsnModel(BaseModel):
    url: PostgresDsn


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "database_"

    _dsn: PostgresDsnModel
    driver: str = "postgresql+asyncpg"
    name: str = "currency-exchange"
    username: str = "postgres"
    password: str = "password"
    host: str = "localhost"
    port: int = 5432
    echo: bool = False

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "DatabaseSettings":
        url: PostgresDsn = PostgresDsn.build(
            scheme=self.driver,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )
        self._dsn = PostgresDsnModel(url=url)
        return self

    @property
    def url(self) -> str:
        return self._dsn.url.unicode_string()


app_settings = AppSettings()
database_settings = DatabaseSettings()
