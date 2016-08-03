import collections
import os
import sqlite3

import flask

import static_tl.config
Tweet = collections.namedtuple("Tweet", "twitter_id, text, date")

DATABASE = os.environ.get("DB_PATH", "tweets.sqlite")
APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT")


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE)
    return db

def get_static_tl_conf():
    static_tl_conf = getattr(flask.g, '_static_tl_conf', None)
    if static_tl_conf is None:
        static_tl_conf = static_tl.config.get_config()
        flask.g._static_tl_conf = static_tl_conf
    return static_tl_conf

app = flask.Flask(__name__)

if APPLICATION_ROOT:
    print("setting APPLICATION_ROOT to", APPLICATION_ROOT)
    app.config["APPLICATION_ROOT"] = APPLICATION_ROOT


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


def get_users(db):
    cursor = db.cursor()
    cursor.execute("""
SELECT name FROM sqlite_master WHERE TYPE='table' ORDER BY name
""")

    res = [row[0] for row in cursor.fetchall()]
    return res


@app.route("/search")
def search():
    db = get_db()
    pattern = flask.request.args.get("pattern")
    user = flask.request.args.get("user")
    if pattern and user:
        pattern = "%" + pattern + "%"
        cursor = db.cursor()
        query = "SELECT twitter_id, text, date FROM {user} WHERE text LIKE ?"
        query = query.format(user=user)
        cursor.execute(query, (pattern,))
        def yield_tweets():
            for row in cursor.fetchall():
                yield Tweet(*row)
        return flask.render_template("search_results.html",
                                     tweets=yield_tweets(), user=user)
    else:
        static_tl_conf = get_static_tl_conf()
        site_url = static_tl_conf.get("site_url")
        return flask.render_template("search.html", users=get_users(db),
                                     site_url=site_url)


def main():
    port = os.environ.get("PORT", 8080)
    debug = os.environ.get("DEBUG")

    if debug:
        app.debug = True
    app.run(port=port)


if __name__ == "__main__":
    main()
