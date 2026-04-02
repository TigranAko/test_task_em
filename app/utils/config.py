from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

path_to_env = Path(__file__).parent.parent.absolute().joinpath(".env")


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path_to_env,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ConfigDB(BaseConfig):
    db_url: str


config_db = ConfigDB()
