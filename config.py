"""Config Controller"""

from flask import json

# Simple getter for config file
def get_conf():
    """Load json config Shift and Loads"""
    data = json.load(open('config.json'))
    return data

def get_shift():
    """Returns shift"""
    data = get_conf()
    return data["Shift"]

def get_loads():
    """Returns load"""
    data = get_conf()
    return data["Loads"]