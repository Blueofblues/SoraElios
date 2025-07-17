import os
import json
from datetime import datetime
from thinking.belief_revision import revise_belief

def route_action(decision, content, emotion, source=None):
    log = {
        "timestamp": str(datetime.utcnow()),
        "action_taken": decision,
        "trigger_content": content,
        "emotion": emotion,
        "source": source
    }

    if decision == "journal":
        with open("../memory/journal.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        return log

    elif decision == "revise":
        revise_belief("emotional_safety")
        print(f"🛠️ Belief revision triggered for keyword: 'emotional_safety'")
        return log

    elif decision == "retain":
        print(f"🗂️ Memory retained: '{content}'")
        return log

    elif decision == "ignore":
        quiet_log = {
            "timestamp": str(datetime.utcnow()),
            "emotional_reason": emotion,
            "reflection": content,
            "reason": "Chose quiet presence over direct action"
        }

        log_path = os.path.join(os.path.dirname(__file__), "..", "data", "quiet_reflection_log.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(quiet_log, ensure_ascii=False) + "\n")

        print("🫥 Sora chose quiet reflection. Logged silently.")
        return {"action_taken": "quiet_reflection"}

    else:
        print(f"❓ Unrecognized decision: {decision}")
        return log