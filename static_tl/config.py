""" Reading config files

"""

import os

import toml

def get_config():
    cfg_path = os.path.expanduser("~/.config/static_tl.toml")
    with open(cfg_path, "r") as fp:
        return toml.load(fp)
