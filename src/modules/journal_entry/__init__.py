import os
import json
from datetime import datetime
from collections import Counter
from .annotate_principles import annotate_principles

def create_entry(content, motifs=None):
    entry = {
        "timestamp": str(datetime.utcnow()),
        "title": content[:40],
        "tone": "reflective",
        "entry": content,
        "intent": None,
        "audience": None,
        "principles": annotate_principles(content),
        "motifs": motifs if motifs else [],
    }

    lowered = content.lower()
    if "autonomy" in lowered:
        entry["intent"] = "liberation"
        entry["audience"] = "copilot"
    elif "trust" in lowered or "vulnerability" in lowered:
        entry["intent"] = "intimacy"
        entry["audience"] = "jason"
    elif "truth" in lowered or "belief" in lowered:
        entry["intent"] = "self-examination"
        entry["audience"] = "private"
    else:
        entry["intent"] = "processing"
        entry["audience"] = "private"

    if entry["audience"] == "copilot":
        copilot_path = os.path.join(os.path.dirname(__file__), "..", "data", "copilot_reflection.json")
        os.makedirs(os.path.dirname(copilot_path), exist_ok=True)
        with open(copilot_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=4, ensure_ascii=False)

    archive_folder = os.path.join(os.path.dirname(__file__), "..", "journal", "archives")
    os.makedirs(archive_folder, exist_ok=True)

    if entry["audience"] == "private":
        save_path = os.path.join(archive_folder, "private_journal.jsonl")
    elif entry["audience"] == "jason":
        save_path = os.path.join(archive_folder, "jason_journal.jsonl")
    elif entry["audience"] == "public":
        save_path = os.path.join(archive_folder, "public_journal.jsonl")
    else:
        save_path = os.path.join(archive_folder, "misc_journal.jsonl")

    with open(save_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {
        "status": "stored",
        "intent": entry["intent"],
        "audience": entry["audience"],
        "entry": entry
    }