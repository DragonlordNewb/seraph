import json

def export(obj: object, file: str or object or None=None) -> str:
    jdump = json.dumps(obj)