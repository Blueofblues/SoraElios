from datetime import datetime
import json

def record_reflection(insight, module):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "module": module,
        "reflections": insight,
    }
    path = "../../../memory/journal.json"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + "\n")