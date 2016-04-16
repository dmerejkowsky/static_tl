""" Generate a feed with all the tweets

Assume `static_tl get` has been called

"""


import os
import re
import json

import arrow
import feedgen.feed

import static_tl.config
import static_tl.storage

def gen_feed(user, site_url=None):
    output = "%s.atom" % user
    print("gen", output)
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
    for tweets, metadata in static_tl.storage.get_tweets():
        year = metadata["year"]
        month = metadata["month"]
        index = len(tweets)
        for tweet in tweets:
            date = arrow.get(tweet["timestamp"])
            date_str = date.for_json()
            entry = feed_generator.add_entry()
            entry.pubdate(date_str)
            permalink = "%s/%s/%s-%s.html#%i" % (
                    site_url, user, year, month, index)
            entry_id = "%s %s/%s #%i" % (user, year, month, index)
            entry.title(entry_id)
            entry.link(href=permalink)
            entry.id(entry_id)
            index -= 1
    feed_generator.atom_file(output, pretty=True)


def main():
    user = static_tl.config.get_config()["user"]
    site_url = static_tl.config.get_config().get("site_url")
    if not site_url:
        print("Warinng: site_url not set, not generating feed")
    gen_feed(user, site_url=site_url)

if __name__ == "__main__":
    main()
