import psycopg
#from psycopg import extras
from contextlib import contextmanager

from config import Config

config = Config()

@contextmanager
def get_conn(cfg: Config):
    """Открывает соединение, коммитит при успехе, роллбэчит при ошибке, всегда закрывает."""
    conn = psycopg.connect(**cfg.db_params)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(cfg: Config):
    with get_conn(cfg) as conn:
        with conn.cursor() as cursor: # посмотреть у Дани
            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            login TEXT,
            hashed_password TEXT NOT NULL,
            name TEXT,
            email TEXT,
            is_verified BOOLEAN DEFAULT FALSE
            );
            """
                           )
            if config.mode == "test":
                cursor.execute(
                    """
                    INSERT INTO users(login, hashed_password, name, email) VALUES(%s, %s, %s, %s)
                    """, ("testuser", "hashedpasswordlol", "test", "t@t.t")
                )
    print("DB initialized")

init_db(config)