""" Reading config files

"""

import os
import configparser

def get_config():
    cfg_path = os.path.expanduser("~/.config/twitt-back.cfg")
    parser = configparser.ConfigParser()
    parser.read(cfg_path)
    return parser["twitt-back"]
