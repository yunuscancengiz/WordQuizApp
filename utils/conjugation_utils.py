import os
import json


def load_json_data():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'verbs.json')
    with open(json_path, mode='r', encoding='utf-8') as f:
        try:
            verb_data = json.load(f)
        except json.JSONDecodeError:
            verb_data = {"verbs": {}}
    return verb_data