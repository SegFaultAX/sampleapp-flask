import db

@db.with_pool
def create_articles_table(conn):
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      content TEXT
    );
  """)
  conn.commit()

MIGRATIONS = [
  create_articles_table,
]

if __name__ == "__main__":
  for migration in MIGRATIONS:
    print "Running migration: %s" % migration.func_name
    migration()
