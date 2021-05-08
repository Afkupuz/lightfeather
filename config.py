"""Config Controller"""

from flask import json

def get_conf():
    """Load json config Shift and Loads"""
    data = json.load(open('config.json'))
    return data

def get_shift():
    data = get_conf()
    return data["Shift"]

def get_loads():
    data = get_conf()
    return data["Loads"]