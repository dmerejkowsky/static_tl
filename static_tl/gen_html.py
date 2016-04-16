""" Generate a static html site containing all the tweets.

Assume `static_tl get` has been called

"""

import os

import arrow
import jinja2

import static_tl.config
import static_tl.storage

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
        tweet["date"] = date.strftime("%a %d %H:%m")
        tweet["text_as_html"] = tweet["text"]
        gen_text_as_html(tweet)

def gen_from_template(out, template_name, context):
    print("gen", out)
    loader = jinja2.PackageLoader("static_tl", "templates")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
    to_write = template.render(**context)
    with open(out, "w") as fp:
        fp.write(to_write)

def gen_page(tweets, metadata):
    context = metadata
    month_number =  metadata["month"]
    context["month_short_name"] = get_month_short_name(month_number)
    page_name = "%s-%s.html" % (metadata["year"], month_number)
    out = "html/%s" % page_name
    fix_tweets(tweets)
    context["tweets"] = tweets
    gen_from_template(out, "by_month.html", context)
    return page_name

def gen_index(all_pages):
    out = "html/index.html"
    context = dict()
    context["pages"] = all_pages
    gen_from_template(out, "index.html", context)
    return out

def gen_html(user, site_url=None):
    if not os.path.exists("html"):
        os.mkdir("html")

    all_pages = list()
    for tweets, metadata in static_tl.storage.get_tweets():
        metadata["site_url"] = site_url
        metadata["user" ] = user
        page_name = gen_page(tweets, metadata)
        page = dict()
        page["href"] = page_name
        page["metadata"] = metadata
        all_pages.append(page)
    gen_index(all_pages)


def main():
    user = static_tl.config.get_config()["user"]
    site_url = static_tl.config.get_config().get("site_url")
    if not site_url:
        print("Warinng: site_url not set, permalinks won't work")
    gen_html(user, site_url=site_url)
    print("Site generated in html/")

if __name__ == "__main__":
    main()
