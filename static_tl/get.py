"""
Dump all tweets to several .json file, suitable for
a static site generation.

Work incrementally, by looking at the last status ID
in the most recent .json file: this allows you edit your tweets :)

If you run this for the first time we will fetch
an hard-coded number of tweets.

"""

import argparse
import itertools
import json
import os

import arrow
import twitter

import static_tl.config

MAX_TWEETS = 3000 # Just an arbitrary limit ...

def get_credentials(config):
    """ Get the 4 values required for twitter auth

    """
    # TODO: Use keyring instead ? But it requires having
    # gnome-keyring or ksecretservice running ...
    config = static_tl.config.get_config()
    keys = ["token", "token_secret",
            "api_key", "api_secret"]
    return (config[key] for key in keys)

def set_date(tweet):
    """ A a simple 'timestamp' field to the tweet
    object, and return the date as an arrow object
    """
    created_at = tweet['created_at']
    # note : requires https://github.com/crsmithdev/arrow/pull/321
    # date = arrow.get(created_at, 'ddd MMM DD HH:mm:ss Z YYYY')
    date = arrow.Arrow.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
    tweet["timestamp"] = date.timestamp
    return date

def get_new_tweets(user, twitter_api, last_id=None):
    """ Yiels a list of tweets more recent than 'last_id',
    or if last_id is None, the MAX_TWEETS
    """
    tweets = twitter_api.statuses.user_timeline(
        screen_name=user, count=MAX_TWEETS)
    for tweet in tweets:
        date = set_date(tweet)
        if last_id and tweet["id"] <= last_id:
            break
        yield tweet

def group_tweets_by_date(tweets):
    def date_key(tweet):
        timestamp = tweet["timestamp"]
        date = arrow.get(timestamp)
        return (date.year, date.month)
    return itertools.groupby(tweets, key=date_key)


def dump(user, tweets):
    """ Dump retrieved tweets for the given user

    Return number of tweets written
    """
    n = 0
    output_dir = "json/%s" % user
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass
    by_date = group_tweets_by_date(tweets)
    for (year, month), tweets in by_date:
        tweets = list(tweets)
        n += len(tweets)
        output_name = "%i-%02i.json" % (year, month)
        output = os.path.join(output_dir, output_name)
        if os.path.exists(output):
            with open(output, "r") as fp:
                previous_tweets = json.load(fp)
        else:
            previous_tweets = list()
        with open(output, "w") as fp:
            new_tweets = tweets + previous_tweets
            json.dump(new_tweets, fp, indent=2)
            print("Tweets written to", output)
    return n

def main():
    config = static_tl.config.get_config()
    auth_dict = config["auth"]
    keys = ["token", "token_secret",
            "api_key", "api_secret"]
    auth_values = (auth_dict[key] for key in keys)
    auth = twitter.OAuth(*auth_values)
    api = twitter.Twitter(auth=auth)
    users = sorted(config["users"][0].keys())
    for user in users:
        print("Getting tweets from", user)
        last_id = static_tl.storage.get_last_id(user)
        new_tweets = get_new_tweets(user, api, last_id=last_id)
        n_tweets = dump(user, new_tweets)
        if n_tweets:
            print("Written %i new tweets" % n_tweets)
        else:
            print("No new tweets found")

if __name__ == "__main__":
    main()
