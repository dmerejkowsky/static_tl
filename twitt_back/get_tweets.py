"""
Dump all tweets to a .json file, suitable for
a static site generation

You should run this at least once a month

For instance, if your un it on 2016 October 10, you'll get two
files:
    tweets-<user>-2016-09.json # all the tweets from September
    tweets-<user>-2016-10.json # all the tweets this month

(the last file will be overridden when you'll re-run the
script in November)

Of course, you should keep the .json files, and then
run gen_htlm() with all your .json data ...

"""

import argparse
import json
import os

import arrow
import twitter

API_KEY = "7kiffT1EnER5sQGz9WMepBzjB"
ACCESS_TOKEN = "468504845-v2ThgjVsjFjOsFILOVykyW4CF664g4OXXx2TwYlA"
MAX_TWEETS_IN_TWO_MONTHS = 30 * 100 * 2# One hundred per day !


def get_secrets():
    """ Get the secret token and the api secret  from
    a config file (in clear text)

    """
    # TODO: Use keyring instead ? But it requires having
    # gnome-keyring or ksecretservice running ...
    config = get_config()
    return (config["token_secret"], config["api_secret"])

def last_two_months():
    now = arrow.now()
    last_month = now.replace(months=-1)
    return(now, last_month)


def set_date(tweet):
    """ A a simple 'timestamp' field to the tweet
    object, and return the date as an arrow object
    """
    # note : requires https://github.com/crsmithdev/arrow/pull/321
    created_at = tweet['created_at']
    date = arrow.get(created_at, 'ddd MMM DD HH:mm:ss Z YYYY')
    tweet["timestamp"] = date.timestamp
    return date

def get_tweets_since_last_month(twitter_api):
    """ Return two lists of two lists of two elements:

    [
        [this_month, [the (possibly) incomplete list of tweets from this month]]
        [last_month, [the complete list tweets from last month])],
    ]

    """
    user = get_config()["user"]
    (now, a_month_ago) = last_two_months()
    res = [[now, list()], [a_month_ago, list()]]
    tweets = twitter_api.statuses.user_timeline(
        screen_name=user, count=MAX_TWEETS_IN_TWO_MONTHS)
    for tweet in tweets:
        date = set_date(tweet)
        if date.month == now.month:
            res[0][1].append(tweet)
        elif date.month == a_month_ago.month:
            res[1][1].append(tweet)
        else:
            break
    return res

def dump(tweets):
    for (date, tweets_this_date) in tweets:
        output = "tweets-%i-%02i.json" % (date.year, date.month)
        with open(output, "w") as fp:
            json.dump(tweets_this_date, fp, indent=2)
            print("Tweets backed up to", output)

def main():
    token_secret, api_secret = get_secrets()
    auth = twitter.OAuth(ACCESS_TOKEN, token_secret,
        API_KEY, api_secret)
    api = twitter.Twitter(auth=auth)
    tweets_since_last_month = get_tweets_since_last_month(api)
    dump(tweets_since_last_month)

if __name__ == "__main__":
    main()
