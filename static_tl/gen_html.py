""" Generate a static html page containing all the tweets.

Assume `static_tl get` has been called

"""

import os
import re
import json

import arrow
import jinja2

import static_tl.config

JSON_FILENAME_RE = re.compile(r"""
    tweets-
    (?P<year>(\d{4}))-       # Year is four digits
    (?P<month>(\d{2}))       # Month is two digits (01-12)
    \.json                   # Extension
""", re.VERBOSE)

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

def gen_page(json_file, metadata):
    context = metadata
    month_number =  metadata["month"]
    page_name = "%s-%s.html" % (metadata["year"], month_number)
    out = "html/%s" % page_name
    with open(json_file, "r") as fp:
        tweets =  json.load(fp)
    fix_tweets(tweets)
    context["tweets"] = tweets
    date = arrow.Arrow(year=2000, day=1, month=int(month_number))
    context["month_short_name"] = date.strftime("%b")
    gen_from_template(out, "by_month.html", context)
    return page_name

def gen_index(all_pages):
    out = "html/index.html"
    context = dict()
    context["pages"] = all_pages
    gen_from_template(out, "index.html", context)
    return out

def gen_html(site_url=None):
    if not os.path.exists("html"):
        os.mkdir("html")
    all_pages = list()
    for filename in sorted(os.listdir("."), reverse=True):
        match = re.match(JSON_FILENAME_RE, filename)
        if match:
            metadata = match.groupdict()
            metadata["site_url"] = site_url
            page_name = gen_page(filename, metadata)
            page = dict()
            page["href"] = page_name
            page["metadata"] = metadata
            all_pages.append(page)
    gen_index(all_pages)


def main():
    site_url = static_tl.config.get_config().get("site_url")
    if not site_url:
        print("Warinng: site_url not set, permalinks won't work")
    gen_html(site_url=site_url)
    print("Site generated in html/")

if __name__ == "__main__":
    main()
