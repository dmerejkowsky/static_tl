""" Generate a static html site from your tweets

Two commands to run, every month:

    static_tl get    # stores your latest tweets in .json files
    static_tl gen    # gen a static html web site using the generated .json files

"""

USAGE = """ Usage: static_tl [-h] {help,get,gen} """

import sys

from static_tl.get_tweets import main as main_get
from static_tl.gen_html import main as main_gen

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit("Missing argument")
    if len(sys.argv) > 2:
        print(USAGE)
        sys.exit("Too many arguments")

    if sys.argv[1] in ["-h", "--help", "help"]:
        print(USAGE)
        sys.exit(0)

    if sys.argv[1] == "get":
        main_get()
        sys.exit(0)

    if sys.argv[1] == "gen":
        main_gen()
        sys.exit(0)
