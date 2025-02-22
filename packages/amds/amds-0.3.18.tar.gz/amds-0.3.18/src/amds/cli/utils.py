import json


def print_json(data):
    """Print data as formatted JSON"""
    # If the data has a 'result' field, only print that
    if isinstance(data, dict) and "result" in data:
        print(json.dumps(data["result"], indent=2))
    else:
        print(json.dumps(data, indent=3))
