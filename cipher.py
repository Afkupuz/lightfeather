
"""cipher controller"""

from flask import json

LOWER_STRING = "abcdefghijklmnopqrstuvwxyz"
UPPER_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_STRING = "1234567890"
OTHER_STRING = "!@#$%^&*()"

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

def encode(text):
    """Shifts forward each character in text by Shift amount"""
    shift = abs(get_shift())
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

def write_to_file(text):
    path = get_loads()
    storage_file = open(path, "w")
    encoded = encode(text)
    storage_file.writelines(encoded)
    storage_file.close()
    return True

def read_from_file():
    data = []
    path = get_loads()
    storage_file = open(path, "r")
    for line in storage_file:
        data.append(decode(line))
    storage_file.close()
    return data


write_to_file("Hello world")
print(read_from_file())