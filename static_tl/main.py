""" Generate a static html site from your tweets

Two commands to run, every month:

    static_tl get    # stores your latest tweets in .json files
    static_tl gen    # gen a static html web site using the generated .json files

"""


import argparse
import cgitb
import os

from static_tl.get import main as main_get
from static_tl.gen import main as main_gen

def main():
    cgitb.enable(logdir=os.getcwd(), format="txt")
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="avaible actions",
                                       dest="action")
    subparsers.add_parser("get")
    subparsers.add_parser("gen")
    args = parser.parse_args()
    if args.action == "get":
        main_get()
    elif args.action == "gen":
        main_gen()
