import json


def ping_back(payload):
    response = {"mode": "ping", "message": "hello back..."}
    return json.dumps(response)
