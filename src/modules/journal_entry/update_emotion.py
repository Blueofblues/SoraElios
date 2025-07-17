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