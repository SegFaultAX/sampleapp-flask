import db

MIGRATIONS = []

def migration(fn):
  MIGRATIONS.append(fn)
  return fn

def _run_migrations():
  for migration in MIGRATIONS:
    print "Running migration: %s" % migration.func_name
    migration()

@migration
@db.with_pool
def create_updated_at_function(conn):
  cursor = conn.cursor()
  cursor.execute("""
    CREATE OR REPLACE FUNCTION auto_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = now();
      RETURN NEW;
    END;
    $$ language 'plpgsql';
  """)
  conn.commit()

@migration
@db.with_pool
def create_articles_table(conn):
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      content TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX idx_articles_updated_at_desc ON articles (updated_at DESC);

    CREATE TRIGGER update_articles_updated_at_time BEFORE UPDATE
    ON articles FOR EACH ROW EXECUTE PROCEDURE auto_updated_at_column();
  """)
  conn.commit()

if __name__ == "__main__":
  _run_migrations()
