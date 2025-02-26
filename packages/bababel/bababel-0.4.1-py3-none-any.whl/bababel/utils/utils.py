import json


def dict_to_bytes(body: dict) -> bytes:
    json_str = json.dumps(body)
    return json_str.encode("utf-8")
