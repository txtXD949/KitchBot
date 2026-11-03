# DBOperations/migrations/db_migration.py
from pathlib import Path

from yoyo import get_backend, read_migrations

from ..config import get_config


def migrate() -> None:
    cfg = get_config()
    p = cfg.db_params  # dict с host/port/user/password/dbname
    url = (
        f"postgresql+psycopg://{p['user']}:{p['password']}"
        f"@{p['host']}:{p['port']}/{p['dbname']}"
    ) # Берет данные напрямую из конфига. 

    backend = get_backend(url)
    migrations = read_migrations(str(Path(__file__).parent / "sql"))

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


if __name__ == "__main__":
    migrate()