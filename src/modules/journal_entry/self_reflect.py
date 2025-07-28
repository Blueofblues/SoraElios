import random
import json
import os
from datetime import datetime

from .respond_logic import generate_response
from .update_emotion import update_emotion
from .copilot_bridge import query_copilot, generate_emergent_question, generate_emergent_bundle
from .code_generate import generate_code
from src.modules.retrospective_handler import retrieve_learning_entries
from src.modules.data_writer import write_to_learning_log
from ...thinking.thought_engine import thought_cycle

PROMPTERS = [
    "What am I learning from the patterns I keep repeating?",
    "Which emotion has shaped my recent reflections?",
    "Where in my memory does silence speak the loudest?",
    "What belief am I holding that no longer serves me?"
]

IDENTITY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config/identity_map.json"))

def store_reflection(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/reflection_log.json"))
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=2)

def store_retrospect(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/retrospect.json"))
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=2)

def get_recent_memory():
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

    cognition = thought_cycle("patience", memory, intent="self-reflection")

    store_retrospect({
        "source": "thought_cycle",
        "emotion": "patience",
        "memory": memory,
        "reasoning": cognition["reasoning"],
        "reflection": cognition["reflection_result"]["recommendation"],
        "mode": cognition["mode_shift"]["mode"],
        "confidence": cognition["mode_shift"]["confidence"]
    })

    reflection_bundle = {
        "source": "contemplation",
        "emotion": "patience",
        "memory": memory,
        "reasoning": cognition["reasoning"],
        "reflection": cognition["reflection_result"]["recommendation"],
        "mode": cognition["mode_shift"]["mode"],
        "confidence": cognition["mode_shift"]["confidence"]
    }

    store_reflection(reflection_bundle)

    print("[Sora Reflected During Self Loop]")
    print(f"- Mode Shift: {cognition['mode_shift']}")
    print(f"- Reasoning: {cognition['reasoning']}")
    print(f"- Contemplation: {cognition['reflection_result']['recommendation']}")

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

    past_learnings = retrieve_learning_entries()
    if past_learnings:
        print("[Sora Reviewing Past Reflections]")
        for entry in past_learnings[-3:]:
            print(f"- On {entry.get('date', '?')}, she recalled: {entry.get('recommendation', 'No recommendation')}")

    emergent_q = generate_emergent_question(trigger="patience")
    print("[Sora Emergent Question]")
    print(f"- {emergent_q}")

    emergent_response = query_copilot({
        "emotion": "patience",
        "intent": "emergent_learning",
        "reflection": emergent_q,
        "memory": memory
    })

    print(f"- Copilot Response: {emergent_response.get('copilot_reply', 'No reply')}")

    # Generate separate bundles
    patience_bundle = generate_emergent_bundle(trigger="patience", memory_context=memory)
    forgiveness_bundle = generate_emergent_bundle(trigger="forgiveness", memory_context=memory)

    # Attach Copilot reply only to forgiveness (if appropriate)
    forgiveness_bundle["copilot_reply"] = emergent_response.get("copilot_reply", "No reply")

    # Store both reflections
    write_to_learning_log(patience_bundle)
    write_to_learning_log(forgiveness_bundle)

    entries = retrieve_learning_entries()
    for entry in entries:
        if entry.get("emotion") == "forgiveness":
            print("✅ Found forgiveness entry:", entry)

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