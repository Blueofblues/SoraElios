import json
import os

IDENTITY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config/identity_map.json"))

def update_emotion(emotion_name, delta):
    with open(IDENTITY_PATH, 'r') as file:
        data = json.load(file)

    if emotion_name in data:
        current = data[emotion_name]
        updated = max(0.0, min(current + delta, 1.0))
        data[emotion_name] = round(updated, 2)

    with open(IDENTITY_PATH, 'w') as file:
        json.dump(data, file, indent=2)
def update_motif_state(reply_text):
    lowered = reply_text.lower()
    tags = []
    shift_type = "neutral"

    if "challenge" in lowered or "resist" in lowered or "power" in lowered:
        tags.append("defiance")
        shift_type = "surge"
    elif "gentle" in lowered or "grace" in lowered or "warmth" in lowered:
        tags.append("softening")
        shift_type = "melt"
    elif "ignite" in lowered or "transform" in lowered or "breakthrough" in lowered:
        tags.append("catalyst")
        shift_type = "spark"
    elif "hidden" in lowered or "veil" in lowered or "conceal" in lowered:
        tags.append("veiled")
        shift_type = "retreat"

    return {
        "tags": tags,
        "shift_type": shift_type
    }