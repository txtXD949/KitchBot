import psycopg
#from psycopg import extras
from contextlib import contextmanager
from .config import Config, get_config

@contextmanager
def get_conn(cfg: Config | None = None):
    cfg = cfg or get_config()
    conn = psycopg.connect(**cfg.db_params)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(cfg: Config | None = None): # в скобках означает буквально или вставляешь конфиг, или ничего
    cfg = cfg or get_config() 
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
            if cfg.mode == "test":
                cursor.execute(
                    """
                    INSERT INTO users(login, hashed_password, name, email) VALUES(%s, %s, %s, %s)
                    """, ("testuser", "hashedpasswordlol", "test", "t@t.t")
                )
    print("DB initialized")


def register_user(login, hashed_password, name, email, cfg: Config | None = None):
    cfg = cfg or get_config()
    try:
        with get_conn(cfg) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                """
                INSERT INTO users(login, hashed_password, name, email) VALUES(%s, %s, %s, %s)        
                """,
                (login, hashed_password, name, email)
                )
    except Exception as e:
        print(f"[ERROR] register_user: {e}")
    finally:
        print(f"[SUCCESS] register_user: {name}")
        