import os
import sqlite3

import flask

DB_PATH = os.environ.get("DB_PATH", "tweets.sqlite")
CONNECTION = sqlite3.connect(DB_PATH)


app = flask.Flask("static_tl_search")

@app.route("/search")
def search():
    print(flask.request.args)
    pattern = flask.request.args.get("pattern")
    user = flask.request.args.get("user")
    if pattern:
        pass
    else:
        return flask.render_template("search.html")


def main():
    port = os.environ.get("PORT", 8080)
    debug = os.environ.get("DEBUG")
    if debug:
        app.debug = True
    app.run(port=port)

if __name__ == "__main__":
    main()
