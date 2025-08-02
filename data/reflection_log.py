import os
import json

REFLECTION_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/reflection_log.json")
)

def load_reflections():
    if os.path.exists(REFLECTION_PATH):
        try:
            with open(REFLECTION_PATH, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []