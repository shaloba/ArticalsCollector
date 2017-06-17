import json
from functools import wraps


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return json.loads(func(*args, **kwargs))
        except ValueError:
            return []
    return wrapper