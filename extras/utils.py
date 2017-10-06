import json
from Type import Type


def get_type(string):
    if is_int(string):
        return Type.INT
    elif is_json(string):
        return Type.JSON
    elif is_bool(string):
        return Type.BOOL
    elif is_directory(string):
        return Type.DIRECTORY
    else:
        return Type.STRING


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_json(string):
    try:
        json_object = json.loads(string)
    except ValueError, e:
        return False
    return True


def is_bool(string):
    return (string == "true") or (string == "false")


def is_directory(string):
    return ("/" in string)
