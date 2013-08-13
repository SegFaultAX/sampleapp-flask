import db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack

PORT = 5000
USERNAME = "mkbernard"
PASSWORD = "secret"
DEBUG = True
SECRET_KEY = "foobar"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SAMPLEAPP_SETTINGS', silent=True)

@db.with_pool
def get_articles(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT id, title, content FROM articles LIMIT 10")
  return cursor.fetchall()

@app.route("/")
def index():
  articles = get_articles()
  print articles
  return render_template("index.html", articles=articles)

if __name__ == "__main__":
  app.run()
