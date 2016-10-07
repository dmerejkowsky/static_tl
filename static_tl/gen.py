""" Generate a static html site containing all the tweets.

Assume `static_tl get` has been called

"""

import os
import shutil
import sqlite3

import arrow
import feedgenerator
import jinja2

import static_tl.config
import static_tl.storage


def is_reply(tweet):
    """ Assume a tweet is a reply if in_reply_to_screen_name
    or in_reply_to_status_id are not None

    """
    return tweet.get("in_reply_to_screen_name") or \
            tweet.get("in_reply_to_status_id")


def filter_tweets(user_data, tweets):
    """ Return a generator filtering tweets the user does not
    want to keep

    """
    user_name = user_data["screen_name"]
    config = static_tl.config.get_config()
    user_config = config["users"][0][user_name]
    with_replies = user_config.get("with_replies", False)

    if with_replies:
        return tweets

    res = list()
    for tweet in tweets:
        if not(is_reply(tweet)):
            res.append(tweet)
    return res


def get_month_name(month_number):
    """
    >>> get_month_short_name(4)
    'April'

    """
    date = arrow.Arrow(year=2000, day=1, month=int(month_number))
    return date.strftime("%B")


def fix_tweet_text(tweet):
    """ Take the raw text of the tweet and make it better """
    # note : every function will modify tweet["fixed_text"] in place
    tweet["fixed_text"] = tweet["text"]

    # currently we just rewrite all URLs, so that we don't hit
    # http://t.co ..
    fix_urls(tweet) # need to do this first because we need the indices


def fix_urls(tweet):
    """ Replace all the http://t.co URL with their real value """
    orig = tweet["fixed_text"]
    to_do = dict()
    for url in tweet["entities"]["urls"]:
        expanded_url = url["expanded_url"]
        display_url = url["display_url"]
        replacement_str = '<a href="{0}">{1}</a>'.format(expanded_url, display_url)
        start, end = url["indices"]
        to_do[start] = (end, replacement_str)
    new_str = ""
    i = 0
    while i < len(orig):
        if i in to_do:
            end, replacement_str = to_do[i]
            for c in replacement_str:
                new_str += c
                i = end
        else:
            new_str += orig[i]
            i += 1

    tweet["fixed_text"] = new_str


def fix_tweets(tweets):
    """ Add missing metadata, replace URLs, ... """
    for tweet in tweets:
        date = arrow.get(tweet["timestamp"])
        # Maybe this does not belong here ...
        tweet["date"] = date.strftime("%Y %a %B %d %H:%m")
        fix_tweet_text(tweet)


def gen_from_template(out, template_name, context):
    print("Generating", out)
    loader = jinja2.PackageLoader("static_tl", "templates")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
    to_write = template.render(**context)
    with open(out, "w") as fp:
        fp.write(to_write)


def gen_user_page(user_data, tweets, metadata):
    user_name = user_data["screen_name"]
    context = metadata
    month_number =  metadata["month"]
    context["month_name"] = get_month_name(month_number)
    page_name = "%s-%s.html" % (metadata["year"], month_number)
    out = "html/%s/%s" % (user_name, page_name)
    tweets = filter_tweets(user_data, tweets)
    fix_tweets(tweets)
    context["tweets"] = tweets
    context["user"] = user_data
    gen_from_template(out, "by_month.html", context)
    return page_name


def gen_user_index(user_data, all_pages, site_url=None):
    user_name = user_data["screen_name"]
    out = "html/%s/index.html" % user_name
    context = dict()
    context["pages"] = all_pages
    context["user"] = user_data
    context["site_url"] = site_url
    gen_from_template(out, "user_index.html", context)
    return out


def gen_user_pages(user_data, site_url=None):
    user_name = user_data["screen_name"]
    output_dir = os.path.join("html", user_name)
    os.makedirs(output_dir, exist_ok=True)

    all_pages = list()
    for tweets, metadata in static_tl.storage.get_tweets(user_name):
        metadata["site_url"] = site_url
        page_name = gen_user_page(user_data, tweets, metadata)
        page = dict()
        page["href"] = page_name
        page["metadata"] = metadata
        all_pages.append(page)
    gen_user_index(user_data, all_pages, site_url=site_url)
    if site_url:
        gen_user_feed(user_data, site_url=site_url)
    else:
        print("Warinng: site_url not set, not generating any feed")


def gen_index(user_names=None, site_url=None):
    output = os.path.join("html", "index.html")
    gen_from_template(output, "index.html",
            {"user_names" : user_names, "site_url": site_url})


def gen_user_feed(user_data, site_url=None, max_entries=100):
    user_name = user_data["screen_name"]
    output = "html/%s/feed.atom" % user_name
    print("Generating", output)
    title = "Tweets from %s" % user_name
    description = title
    feed_self_url = "%s/%s.atom" % (site_url, user_name)
    feed_generator = feedgenerator.Atom1Feed(
            title=title,
            description=description,
            link=site_url,
            feed_url=feed_self_url)

    n = 0
    for tweets, metadata in static_tl.storage.get_tweets(user_name):
        tweets = filter_tweets(user_data, tweets)
        year = metadata["year"]
        month = metadata["month"]
        index = len(tweets)
        for tweet in tweets:
            n += 1
            if n > max_entries:
                break
            fix_tweet_text(tweet)
            date = arrow.get(tweet["timestamp"])
            permalink = "%s/%s/%s-%s.html#%i" % (
                    site_url, user_name, year, month, index)
            entry_id = "%s %s/%s #%i" % (user_name, year, month, index)
            description = tweet["fixed_text"]
            description = "<pre>%s</pre>" % description
            feed_generator.add_item(
                    title=entry_id,
                    link=permalink,
                    description=description,
                    pubdate=date,
                    updated=date,
            )
            index -= 1
    with open(output, "w") as fp:
        feed_generator.write(fp, "utf-8")


def copy_static():
    outdir = "html"
    static_dir = os.path.join(outdir, "static")
    os.makedirs(static_dir, exist_ok=True)
    loader = jinja2.PackageLoader("static_tl", "templates")
    static_files = [x for x in loader.list_templates() if x.startswith("static/")]
    for static_file in static_files:
        manager = loader.manager
        src = manager.resource_filename("static_tl", "templates/%s" % static_file)
        dest = os.path.join(outdir, static_file)
        print("Copying", src, "->", dest)
        shutil.copy(src, dest)



def updatedb(user_data):
    user_name = user_data["screen_name"]
    db_path = "tweets.sqlite"
    print("Updating database for", user_name, "...", end=" ", flush=True)
    db = sqlite3.connect(db_path)

    sql = """\
DROP TABLE IF EXISTS {user_name};

CREATE VIRTUAL TABLE {user_name} USING fts4(
                     twitter_id INTEGER NOT NULL,
                     text VARCHAR(500) NOT NULL,
                     date VARCHAR(30),
                     UNIQUE(twitter_id));


"""
    db.executescript(sql.format(user_name=user_name))
    db.commit()

    def yield_tweets():
        for tweets, metadata in static_tl.storage.get_tweets(user_name):
            tweets = filter_tweets(user_data, tweets)
            fix_tweets(tweets)
            for tweet in tweets:
                fix_tweet_text(tweet)
                yield tweet["id"], tweet["fixed_text"], tweet["date"]

    sql = "INSERT INTO {user_name} (twitter_id, text, date) VALUES (?, ?, ?)"
    sql = sql.format(user_name=user_name)
    db.executemany(sql, yield_tweets())
    db.commit()
    db.close()
    print("done")


def main():
    config = static_tl.config.get_config()
    site_url = config.get("site_url")
    if not site_url:
        print("Warinng: site_url not set, permalinks won't work")
    copy_static()
    user_config = config["users"][0]
    published_user_names = [x for x in user_config
                       if user_config[x].get("publish", True)]
    published_user_names.sort()
    for user_name in published_user_names:
        user_data = static_tl.storage.get_user_data(user_name)
        gen_user_pages(user_data, site_url=site_url)
    gen_index(user_names=published_user_names, site_url=site_url)
    for user_name in user_config:
        user_data = static_tl.storage.get_user_data(user_name)
        updatedb(user_data)


if __name__ == "__main__":
    main()
