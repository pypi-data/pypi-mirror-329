import os, re, time
import json
from gai.lib import constants

# Get JSON FROM ~/.gairc
def get_rc():
    if (not os.path.exists(os.path.expanduser(constants.GAIRC))):
        raise Exception(f"Config file {constants.GAIRC} not found. Please run 'gai init' to initialize the configuration.")
    with open(os.path.expanduser(constants.GAIRC), 'r') as f:
        return json.load(f)

# Get "app_dir" from ~/.gairc
def get_app_path():
    rc = get_rc()
    app_dir=os.path.abspath(os.path.expanduser(rc["app_dir"]))
    return app_dir

