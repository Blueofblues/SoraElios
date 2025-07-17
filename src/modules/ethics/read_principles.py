import json
import os

def load_principles(path=None):
    if path is None:
        path = os.path.join("modules", "ethics", "principle_manifest.json")
    with open(path) as f:
        return json.load(f)