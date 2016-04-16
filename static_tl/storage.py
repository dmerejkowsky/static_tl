""" Storing tweets retrieved from the twitter API

"""

import json
import os
import re

JSON_FILENAME_RE = re.compile(r"""
    tweets-
    (?P<year>(\d{4}))-       # Year is four digits
    (?P<month>(\d{2}))       # Month is two digits (01-12)
    \.json                   # Extension
""", re.VERBOSE)

def get_tweets():
    """ Get tweets from the .json files retrieved with get_tweets.py

    Yield a tuple ([<list of tweets>], { "year" : <year>, "month" : <month number> }
    for every json file in current working directory, most recent tweets
    first
    """
    for filename in sorted(os.listdir("."), reverse=True):
        match = re.match(JSON_FILENAME_RE, filename)
        if match:
            with open(filename, "r") as fp:
                tweets =  json.load(fp)
                yield(tweets, match.groupdict())
