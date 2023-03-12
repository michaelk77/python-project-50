import json


def format_json(diff):
    return json.dumps(diff, sort_keys=True)
