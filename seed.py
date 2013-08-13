from operator import itemgetter
import db

ARTICLES = [
  { "title": "Foobar1", "content": "This is awesome!" },
  { "title": "Foobar2", "content": "This is neato!" },
]

@db.with_pool
def seed_articles(conn):
  sql = """INSERT INTO articles (title, content) VALUES (%s, %s);"""
  cursor = conn.cursor()
  itemsfn = itemgetter("title", "content")
  items = [itemsfn(e) for e in ARTICLES]
  cursor.executemany(sql, items)
  conn.commit()

SEEDS = [
  seed_articles,
]

if __name__ == "__main__":
  for seeder in SEEDS:
    print "Running seeder: %s" % seeder.func_name
    seeder()
