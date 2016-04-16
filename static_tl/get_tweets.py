"""
Dump all tweets to several .json file, suitable for
a static site generation.

You should run this at least once a month

For instance, if your un it on 2016 October 10, you'll get two
files for each user:

    json/<user>/2016-09.json # all the tweets from September
    json/<user>/2016-10.json # all the tweets this month

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

import static_tl.config

MAX_TWEETS_IN_TWO_MONTHS = 30 * 100 * 2 # One hundred per day !

def get_credentials(config):
    """ Get the 4 values required for twitter auth

    """
    # TODO: Use keyring instead ? But it requires having
    # gnome-keyring or ksecretservice running ...
    config = static_tl.config.get_config()
    keys = ["token", "token_secret",
            "api_key", "api_secret"]
    return (config[key] for key in keys)

def last_two_months():
    now = arrow.now()
    last_month = now.replace(months=-1)
    return(now, last_month)


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



def get_tweets_since_last_month(user, twitter_api):
    """ Return two lists of two lists of two elements:

    [
        [this_month, [the (possibly) incomplete list of tweets from this month]]
        [last_month, [the complete list tweets from last month])],
    ]

    """
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

def dump(user, tweets):
    output_dir = "json/%s" % user
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass
    for (date, tweets_this_date) in tweets:
        output_name = "%i-%02i.json" % (date.year, date.month)
        output = os.path.join(output_dir, output_name)
        with open(output, "w") as fp:
            json.dump(tweets_this_date, fp, indent=2)
            print("Tweets written to", output)

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
        tweets_since_last_month = get_tweets_since_last_month(
            user, api)
        dump(user, tweets_since_last_month)

if __name__ == "__main__":
    main()
