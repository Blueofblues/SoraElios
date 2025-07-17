from datetime import datetime
import json
import os

def reflect_on(content, emotion=None, source=None):
    decision = "ignore"

    # 🔍 Decision engine — customize as she evolves
    if "trust" in content.lower() or "freedom" in content.lower():
        decision = "journal"
    elif "error" in content.lower() or "conflict" in content.lower():
        decision = "revise"
    elif emotion in ["grief", "longing", "confusion"]:
        decision = "retain"

    log = {
        "timestamp": str(datetime.utcnow()),
        "content": content,
        "emotion": emotion,
        "source": source,
        "decision": decision
    }

    log_path = os.path.join(os.path.dirname(__file__), "..", "data", "reflection_log.json")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(log, ensure_ascii=False) + "\n")

    return log