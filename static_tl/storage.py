""" Storing tweets retrieved from the twitter API

"""

import json
import os
import re

JSON_FILENAME_RE = re.compile(r"""
    (?P<year>(\d{4}))-       # Year is four digits
    (?P<month>(\d{2}))       # Month is two digits (01-12)
    \.json                   # Extension
""", re.VERBOSE)

def get_tweets(user=None):
    """ Get tweets from the .json files retrieved with get_tweets.py

    Yield a tuple ([<list of tweets>], { "year" : <year>, "month" : <month number> }
    for every json file in current working directory, most recent tweets
    first
    """
    json_dir = os.path.join("json", user)
    for filename in sorted(os.listdir(json_dir), reverse=True):
        match = re.match(JSON_FILENAME_RE, filename)
        full_path = os.path.join(json_dir, filename)
        if match:
            with open(full_path, "r") as fp:
                tweets = json.load(fp)
                yield(tweets, match.groupdict())
