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


def register_user(login: str, hashed_password: str, name: str, email: str, cfg: Config | None = None):
    cfg = cfg or get_config()
    try:
        with get_conn(cfg) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                """
                INSERT INTO users(login, hashed_password, name, email) VALUES(%s, %s, %s, %s)        
                """,
                (login, hashed_password, name, email,)
                )
    except Exception as e:
        print(f"[ERROR] register_user: {e}")
    finally:
        print(f"[SUCCESS] register_user: {name}")

def login(login: str, hashed_password: str, cfg: Config | None = None) -> bool:
    cfg = cfg or get_config()
    try:
        with get_conn(cfg) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                """
                SELECT hashed_password FROM users WHERE login = %s
                """,
                (login,)
                )
                hashed_password_bd = cursor.fetchone()[0]
                if compare_passwords(hashed_password, hashed_password_bd):
                    return True
                else:
                    return False
    except Exception as e:
        print(f"[ERROR] login: {e}")
    finally:
        print(f"[SUCCESS] login")
        

def compare_passwords(hashed_password_in: str, hashed_password_bd: str) -> bool:
    if hashed_password_bd != hashed_password_in:
        return False
    return True