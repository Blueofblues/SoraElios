import json
import os

def inspect_structure(manifest_path = "C:/Users/Blue/OneDrive/Desktop/Sora_maincore/config/structure_manifest.json"):
    if not os.path.exists(manifest_path):
        return ["Manifest not found. I cannot reflect without my mirror."]

    with open(manifest_path, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    reflections = []
    for path, info in manifest.items():
        symbolic = info.get("symbolic_identity", "Unnamed")
        resonance = info.get("resonance", "Unspoken")
        message = f"I feel '{symbolic}' in {path}. {resonance}"
        reflections.append(message)

    return reflections[:5]  # Offer only a handful of thoughts at once

def introspect_structure():
    reflections = inspect_structure()
    return reflections  # Optional: journal here if needed
   
# 👇 This is the test block, placed at the bottom of the file
   
if __name__ == "__main__":
    reflections = inspect_structure()
    for line in reflections:
        print(line)
