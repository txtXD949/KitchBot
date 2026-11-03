from dataclasses import dataclass
from typing import Literal
from dotenv import load_dotenv

import os


load_dotenv()


@dataclass
class Config:
    mode: str = os.getenv("MODE")
    dbname: str = os.getenv("DBNAME")
    user: str = os.getenv("DBUSER")
    password: str = os.getenv("PASSWORD")
    host: str = os.getenv("HOST")
    port: int = os.getenv("PORT")

    def __post_init__(self):
        if self.mode not in ("test", "prod"):
            raise ValueError(f"Unknown mode: {self.mode}")
        #if self.mode == "prod":
         #   self.password = os.environ.get("DB_PASSWORD", self.password)

    @property
    def db_params(self) -> dict:
        return dict(
            dbname=self.dbname, user=self.user,
            password=self.password, host=self.host, port=self.port,
        )

    def connect_db(self):
        import psycopg
        return psycopg.connect(**self.db_params)

# Необходимо для единичной инициализации конфига при помощи DBOperations
_config: Config | None = None # Хранение конфига


def get_config() -> Config: # Создание первого конфига
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(cfg: Config) -> None: # Изменение конфига
    global _config
    _config = cfg