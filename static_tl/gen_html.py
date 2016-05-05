""" Generate a static html site containing all the tweets.

Assume `static_tl get` has been called

"""

import os
import shutil

import arrow
import feedgen.feed
import jinja2

import static_tl.config
import static_tl.storage

def is_reply(tweet):
    """ Assume a tweet is a reply if in_reply_to_screen_name
    or in_reply_to_status_id are not None

    """
    return tweet.get("in_reply_to_screen_name") or \
            tweet.get("in_reply_to_status_id")

def filter_tweets(user, tweets):
    """ Return a generator filtering tweets the user does not
    want to keep

    """
    config = static_tl.config.get_config()
    user_config = config["users"][0][user]
    with_replies = user_config.get("with_replies", False)

    if with_replies:
        return tweets

    res = list()
    for tweet in tweets:
        if not(is_reply(tweet)):
            res.append(tweet)
    return res


def get_month_short_name(month_number):
    """
    >>> get_month_short_name(4)
    'Apr"

    """
    date = arrow.Arrow(year=2000, day=1, month=int(month_number))
    return date.strftime("%b")

def gen_text_as_html(tweet):
    """ Take the raw text of the tweet and make it better """
    # note : every function will modify tweet["text_as_html"] in place
    fix_urls(tweet) # need to do this first because we need the indices
    fix_newlines(tweet)

def fix_urls(tweet):
    """ Replace all the http://t.co URL with their real value """
    orig = tweet["text_as_html"]
    to_do = dict()
    for url in tweet["entities"]["urls"]:
        expanded_url = url["expanded_url"]
        replacement_str = '<a href="{0}">{0}</a>'.format(expanded_url)
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

    tweet["text_as_html"] = new_str

def fix_newlines(tweet):
    tweet["text_as_html"] = tweet["text_as_html"].replace("\n", "<br/>")

def fix_tweets(tweets):
    """ Add missing metadata, replace URLs, ... """
    for tweet in tweets:
        date = arrow.get(tweet["timestamp"])
        # Maybe this does not belong here ...
        tweet["date"] = date.strftime("%a %d %b %H:%m")
        tweet["text_as_html"] = tweet["text"]
        gen_text_as_html(tweet)

def gen_from_template(out, template_name, context):
    print("Generating", out)
    loader = jinja2.PackageLoader("static_tl", "templates")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
    to_write = template.render(**context)
    with open(out, "w") as fp:
        fp.write(to_write)

def gen_user_page(user, tweets, metadata):
    context = metadata
    month_number =  metadata["month"]
    context["month_short_name"] = get_month_short_name(month_number)
    page_name = "%s-%s.html" % (metadata["year"], month_number)
    out = "html/%s/%s" % (user, page_name)
    tweets = filter_tweets(user, tweets)
    fix_tweets(tweets)
    context["tweets"] = tweets
    gen_from_template(out, "by_month.html", context)
    return page_name

def gen_user_index(user, all_pages):
    out = "html/%s/index.html" % user
    context = dict()
    context["pages"] = all_pages
    context["user"] = user
    gen_from_template(out, "user_index.html", context)
    return out

def gen_user_pages(user, site_url=None):
    output_dir = os.path.join("html", user)
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    all_pages = list()
    for tweets, metadata in static_tl.storage.get_tweets(user):
        metadata["site_url"] = site_url
        page_name = gen_user_page(user, tweets, metadata)
        page = dict()
        page["href"] = page_name
        page["metadata"] = metadata
        all_pages.append(page)
    gen_user_index(user, all_pages)
    gen_user_feed(user, site_url=site_url)


def gen_index(users=None):
    output = os.path.join("html", "index.html")
    gen_from_template(output, "index.html",
            { "users" : users })

def gen_user_feed(user, site_url=None, max_entries=100):
    output = "html/%s/feed.atom" % user
    print("Generating", output)
    feed_generator = feedgen.feed.FeedGenerator()
    title = "Tweets from %s" % user
    description = title
    feed_generator.title(title)
    feed_generator.description(description)
    feed_alternate_url = "%s/%s" % (site_url, user)
    feed_self_url = "%s/%s.atom" % (site_url, user)
    feed_generator.link(rel="alternate", href=feed_alternate_url,
            type="text/html")
    feed_generator.link(rel="self", href=feed_self_url,
            type="application/atom+xml")

    feed_generator.id(feed_self_url)
    n = 0
    for tweets, metadata in static_tl.storage.get_tweets(user):
        year = metadata["year"]
        month = metadata["month"]
        index = len(tweets)
        for tweet in tweets:
            n += 1
            if n > max_entries:
                break
            date = arrow.get(tweet["timestamp"])
            date_str = date.for_json()
            entry = feed_generator.add_entry()
            entry.pubdate(date_str)
            entry.updated(date_str)
            permalink = "%s/%s/%s-%s.html#%i" % (
                    site_url, user, year, month, index)
            entry_id = "%s %s/%s #%i" % (user, year, month, index)
            entry.title(entry_id)
            entry.link(href=permalink)
            entry.id(entry_id)
            index -= 1
    feed_generator.atom_file(output, pretty=True)

def copy_static():
    outdir = "html"
    try:
        os.makedirs(outdir)
    except FileExistsError:
        pass
    loader = jinja2.PackageLoader("static_tl", "templates")
    non_html = [x for x in loader.list_templates() if not x.endswith(".html")]
    for resource_name in non_html:
        manager = loader.manager
        src = manager.resource_filename("static_tl", "templates/%s" % resource_name)
        dest = os.path.join(outdir, resource_name)
        print("Copying", src, "->", dest)
        shutil.copy(src, dest)

def main():
    config = static_tl.config.get_config()
    site_url = config.get("site_url")
    if not site_url:
        print("Warinng: site_url not set, permalinks won't work")
    copy_static()
    users = sorted(config["users"][0].keys())
    for user in users:
        gen_user_pages(user, site_url=site_url)
    gen_index(users=users)

if __name__ == "__main__":
    main()
