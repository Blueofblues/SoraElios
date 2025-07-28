import json

def retrieve_learning_entries(trigger=None, intent=None):
    log_path = "src/memory/learning_log.jsonl"
    entries = []

    with open(log_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if trigger and data.get("emotional_trigger") != trigger:
                    continue
                if intent and data.get("intent") != intent:
                    continue
                entries.append(data)
            except json.JSONDecodeError:
                continue

    return entries