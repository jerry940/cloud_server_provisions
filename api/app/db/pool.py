import os
from psycopg2.pool import SimpleConnectionPool

_POOL = None

def get_pool() -> SimpleConnectionPool:
    global _POOL
    if _POOL is None:
        _POOL = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=os.environ["DATABASE_URL"],
        )
    return _POOL

def get_conn():
    pool = get_pool()
    return pool.getconn()

def put_conn(conn):
    pool = get_pool()
    pool.putconn(conn)
