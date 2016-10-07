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


def get_tweets(user):
    """ Get tweets from the .json files retrieved with get_tweets.py

    Yield a tuple ([<list of tweets>], { "year" : <year>, "month" : <month number> }
    for every json file in current working directory, most recent tweets
    first
    """
    for (json_file, metadata) in get_json_files(user):
        with open(json_file, "r") as fp:
            tweets = json.load(fp)
            yield(tweets, metadata)


def get_last_id(user):
    """ Retrieve last stored tweet id for the given user """
    json_files = get_json_files(user)
    try:
        last_json_file, _ = next(json_files)
    except StopIteration:
        return None
    with open(last_json_file, "r") as fp:
        tweets = json.load(fp)
        return tweets[0]['id']


def get_json_files(user):
    """ Return the json files for the given user, associated
    with their metadata (year and month in a dict)

    """
    res = list()
    json_dir = os.path.join("json", user)
    if not os.path.exists(json_dir):
        return list()
    for filename in sorted(os.listdir(json_dir), reverse=True):
        match = re.match(JSON_FILENAME_RE, filename)
        if match:
            full_path = os.path.join(json_dir, filename)
            yield (full_path, match.groupdict())



def get_user_data(name):
    """ Retrieve data about given user """
    json_path = os.path.join("json", name + ".json")
    with open(json_path, "r") as fp:
        return json.load(fp)
