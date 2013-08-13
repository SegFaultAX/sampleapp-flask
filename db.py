import os
import functools

import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import DictCursor

def db_config():
  db_url = os.getenv("DATABASE_URL")
  if db_url:
    return { "dsn": db_url }
  else:
    return {
      "user": "mkbernard",
      "host": "localhost",
      "port": 5432,
      "database": "sampleapp_test"
    }

SQL_CONNECTION = SimpleConnectionPool(5, 15,
  cursor_factory=DictCursor, **db_config())

def with_pool(fn):
  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    conn = SQL_CONNECTION.getconn()
    result = fn(conn, *args, **kwargs)
    SQL_CONNECTION.putconn(conn)
    return result
  return wrapper
