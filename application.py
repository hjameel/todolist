import os

from contextlib import closing
from flask import Flask, request, g, redirect, url_for, render_template, flash
from sqlite3 import dbapi2 as sqlite3

application = Flask(__name__)

application.config.update(dict(
    DATABASE=os.path.join(application.root_path, "todo.db"),
    SECRET_KEY="development key",
    USERNAME="admin",
    PASSWORD="default"
))
application.config.from_envvar("TODO_SETTINGS", silent=True)

def init_db():
    with closing(connect_db()) as db:
        with application.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(application.config["DATABASE"])

@application.before_first_request
def before_first_request():
    init_db()

@application.before_request
def before_request():
    g.db = connect_db()

@application.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()

@application.route("/")
def todo():
    cur = g.db.execute("select id, todo from todos order by id desc")
    todos = [{"id":todo[0], "text":todo[1] } for todo in cur.fetchall()]
    return render_template("layout.html", todos=todos)

@application.route("/add", methods = ["POST"])
def add():
    g.db.execute("insert into todos (todo) values (?)", [request.form["todo"]])
    g.db.commit()
    flash("New card was added")
    return redirect(url_for("todo"))

@application.route("/delete", methods = ["POST"])
def delete():
    g.db.execute("delete from todos where id = ?", [request.form["id"]])
    g.db.commit()
    return redirect(url_for("todo"))

if __name__ == "__main__":
    application.run()
