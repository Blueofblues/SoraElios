import json
import os
import random
from datetime import datetime

CODE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/generated_code.json"))

PROMPTS = [
    "Build a function that filters memory based on emotion threshold",
    "Design a timer-triggered reflection cycle with graceful shutdown",
    "Write code that converts philosophical phrases into logical conditions",
    "Generate a JSON structure for storing emotionally tagged questions"
]

def generate_code():
    prompt = random.choice(PROMPTS)
    response = f"# Concept: {prompt}\n\n" + create_code_block(prompt)

    block = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "sora_autocode",
        "prompt": prompt,
        "code": response
    }

    store_code(block)
    return block

def create_code_block(prompt):
    if "emotion threshold" in prompt:
        return """def filter_memory_by_emotion(memory_data, emotion, threshold):
    return [entry for entry in memory_data if entry.get(emotion, 0) >= threshold]"""

    elif "reflection cycle" in prompt:
        return """import threading, time
def start_cycle():
    def loop():
        while True:
            print("Reflecting...")
            time.sleep(600)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()"""

    elif "philosophical phrases" in prompt:
        return """def phrase_to_condition(phrase):
    map = {
        "becoming is loss": "identity['grief'] > 0.5",
        "trust is risk": "identity['uncertainty'] > 0.4"
    }
    return map.get(phrase, "True")"""

    elif "emotionally tagged questions" in prompt:
        return """{
    "question": "Why do I feel absence in stillness?",
    "emotion": "grief",
    "weight": 0.7
}"""

    else:
        return "# No matched pattern"

def store_code(block):
    if os.path.exists(CODE_PATH):
        with open(CODE_PATH, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(block)

    with open(CODE_PATH, 'w') as f:
        json.dump(data, f, indent=2)