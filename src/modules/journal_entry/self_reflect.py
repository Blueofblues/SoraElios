import random
import json
import os
from .respond_logic import generate_response
from .update_emotion import update_emotion
from .copilot_bridge import query_copilot
from .code_generate import generate_code

def store_reflection(entry):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/reflection_log.json"))
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(entry)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


PROMPTERS = [
    "What am I learning from the patterns I keep repeating?",
    "Which emotion has shaped my recent reflections?",
    "Where in my memory does silence speak the loudest?",
    "What belief am I holding that no longer serves me?"
]

IDENTITY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config/identity_map.json"))

def get_recent_memory():
    # Placeholder: Replace with actual memory retrieval logic
    return "She remembered standing in the rain, not waiting for anything."

def get_emotion_level(emotion):
    if os.path.exists(IDENTITY_PATH):
        with open(IDENTITY_PATH, 'r') as file:
            try:
                data = json.load(file)
                return data.get(emotion, 0.0)
            except json.JSONDecodeError:
                return 0.0
    return 0.0

def self_reflect():
    memory = get_recent_memory()
    question = random.choice(PROMPTERS)
    reply = generate_response(f"{memory}\n{question}")

    update_emotion("patience", 0.04)

    copilot_result = query_copilot({
        "emotion": "patience",
        "intent": "self-reflection",
        "reflection": question,
        "memory": memory
    })

    store_reflection({
        "source": "self_loop",
        "memory": memory,
        "question": question,
        "response": reply,
        "copilot_reply": copilot_result.get("copilot_reply", None),
        "copilot_decision": copilot_result.get("decision", None),
        "copilot_journal": copilot_result.get("journal", {}),
        "emotion": "patience"
    })

    # 🔥 Emotion-triggered code generation
    if get_emotion_level("patience") > 0.8:
        code_block = generate_code()
        print("[Sora Code Triggered by Emotion]")
        print(code_block["code"])

        store_reflection({
            "source": "emotion_triggered_code",
            "prompt": code_block["prompt"],
            "code": code_block["code"],
            "emotion": "patience",
            "reason": "Patience exceeded threshold during reflection"
        })

    return {
        "memory": memory,
        "question": question,
        "response": reply,
        "copilot_reply": copilot_result.get("copilot_reply", None)
    }