"""Cipher controller"""

from config import get_loads, get_shift
from flask import json

LOWER_STRING = "abcdefghijklmnopqrstuvwxyz"
UPPER_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_STRING = "1234567890"
OTHER_STRING = "!@#$%^&*()"

# Encodes data by shifting based on config Shift and above lists based on what kind of character
def encode(text):
    """Shifts forward each character in text by Shift amount"""
    shift = abs(get_shift())
    print(text)
    data = []
    for i in text:
        if i.strip() and i in LOWER_STRING: 
            data.append(LOWER_STRING[(LOWER_STRING.index(i) + shift) % 26]) 
        elif i.strip() and i in UPPER_STRING: 
            data.append(UPPER_STRING[(UPPER_STRING.index(i) + shift) % 26]) 
        elif i.strip() and i in NUMBER_STRING: 
            data.append(NUMBER_STRING[(NUMBER_STRING.index(i) + shift) % 10])
        elif i.strip() and i in OTHER_STRING: 
            data.append(OTHER_STRING[(OTHER_STRING.index(i) + shift) % 10])    
        else:
            data.append(i)
    output = ''.join(data)
    return output

# Decodes data by shifting based on config Shift and above lists based on what kind of character
def decode(text):
    """Shifts back each character in text by Shift amount"""
    shift = abs(get_shift())
    data = []
    for i in text:
        if i.strip() and i in LOWER_STRING: 
            data.append(LOWER_STRING[(LOWER_STRING.index(i) - shift) % 26]) 
        elif i.strip() and i in UPPER_STRING: 
            data.append(UPPER_STRING[(UPPER_STRING.index(i) - shift) % 26])
        elif i.strip() and i in NUMBER_STRING: 
            data.append(NUMBER_STRING[(NUMBER_STRING.index(i) - shift) % 10]) 
        elif i.strip() and i in OTHER_STRING: 
            data.append(OTHER_STRING[(OTHER_STRING.index(i) - shift) % 10])    
        else:
            data.append(i)
    output = ''.join(data)
    return output

# Saves to file
def write_to_file(data):
    """Encodes and writes to Loads file"""
    print("Writing...")
    path = get_loads()
    storage_file = open(path, "w")
    json_text = json.dumps(data)
    encoded = encode(json_text)
    storage_file.writelines(encoded)
    storage_file.close()
    return True

# Reads from saved file
def read_from_file():
    """Reads from Loads file and decodes"""
    print("Reading...")
    path = get_loads()
    storage_file = open(path, "r")
    data = decode(storage_file.read())
    storage_file.close()
    return json.loads(data)
