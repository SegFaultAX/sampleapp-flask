import db

TRUNCATE = ["articles"]
ARTICLES = [
  { "title": "Foobar1", "content": "This is awesome!" },
  { "title": "Foobar2", "content": "This is neato!" },
]

@db.with_pool
def truncate_tables(conn):
  cursor = conn.cursor()
  for table in TRUNCATE:
    cursor.execute("TRUNCATE TABLE %s" % table)
  conn.commit()

@db.with_pool
def seed_articles(conn):
  sql = """INSERT INTO articles (title, content) VALUES (%(title)s, %(content)s);"""
  cursor = conn.cursor()
  cursor.executemany(sql, ARTICLES)
  conn.commit()

SEEDS = [
  truncate_tables,
  seed_articles,
]

if __name__ == "__main__":
  for seeder in SEEDS:
    print "Running seeder: %s" % seeder.func_name
    seeder()
