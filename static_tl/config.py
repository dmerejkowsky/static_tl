""" Reading config files

"""

import os
import configparser

def get_config():
    cfg_path = os.path.expanduser("~/.config/static_tl.cfg")
    parser = configparser.ConfigParser()
    parser.read(cfg_path)
    return parser["static_tl"]
