import os

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sqlite3 import dbapi2 as sqlite3

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "todo.db"),
    SECRET_KEY="development key",
    USERNAME="admin",
    PASSWORD="default"
))
app.config.from_envvar("TODO_SETTINGS", silent=True)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()

@app.route("/")
def todo():
    cur = g.db.execute("select todo from todos order by id desc")
    return render_template("layout.html", todos=cur.fetchall())

@app.route("/add", methods = ["POST"])
def add():
    g.db.execute("insert into todos (todo) values (?)",
            [request.form["todo"]])
    g.db.commit()
    flash("New card was added")
    return redirect(url_for("todo"))

if __name__ == "__main__":
    app.run()
