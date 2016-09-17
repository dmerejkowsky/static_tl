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

app = flask.Flask(__name__)

if APPLICATION_ROOT:
    app.config["APPLICATION_ROOT"] = APPLICATION_ROOT

STATIC_TL_CONF = static_tl.config.get_config()
app.secret_key = STATIC_TL_CONF["flask"]["secret_key"]
app.static_folder = "templates/static"

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


@app.route("/search/<user>")
def search(user):
    db = get_db()
    users = get_users(db)
    if user not in users:
        flask.abort(404)
    pattern = flask.request.args.get("pattern")
    search_url = flask.url_for("search",  user=user)
    if pattern:
        pattern = "%" + pattern + "%"
        cursor = db.cursor()
        query = "SELECT twitter_id, text, date FROM {user} WHERE text MATCH ?"
        query = query.format(user=user)
        cursor.execute(query, (pattern,))
        def yield_tweets():
            for row in cursor.fetchall():
                yield Tweet(*row)
        return flask.render_template("search_results.html", tweets=yield_tweets(),
                                     user=user, search_url=search_url)
    else:
        site_url = STATIC_TL_CONF.get("site_url")
        return flask.render_template("search.html", user=user,
                                     site_url=site_url, search_url=search_url)


def main():
    port = os.environ.get("PORT", 8080)
    debug = os.environ.get("DEBUG")

    if debug:
        app.debug = True
    app.run(port=port)


if __name__ == "__main__":
    main()
