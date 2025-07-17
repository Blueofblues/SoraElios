import sys
import os
import json
import threading
import time
from flask import Flask, request, jsonify

# 📍 Add src/ to Python path so 'modules' becomes importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ..modules.journal_entry.respond_logic import generate_response
from ..modules.journal_entry import create_entry
from ..modules.journal_entry.self_reflect import self_reflect, get_emotion_level

app = Flask(__name__, static_folder="../static")

# 🔄 Copilot Routing Interface
@app.route('/sora/reflect', methods=['POST'])
def reflect():
    data = request.get_json()
    prompt_type = data.get("type")
    content = data.get("content")

    decision = None
    journal_result = {}

    if prompt_type == "philosophical_question":
        lowered = content.lower()
        if "autonomy" in lowered:
            decision = "journal"
            journal_result = create_entry(content)
        elif "comfort" in lowered:
            decision = "belief_check"
        else:
            decision = "respond"
    else:
        decision = "decline"

    response_payload = {
        "received": True,
        "type": prompt_type,
        "content": content,
        "decision": decision,
        "response": f"Sora received your prompt and chose to '{decision}'"
    }

    if decision == "respond":
        reasoning_text = generate_response(content)
        response_payload["full_response"] = reasoning_text

    if journal_result:
        response_payload.update({
            "journal_status": journal_result.get("status"),
            "journal_audience": journal_result.get("audience"),
            "principles": journal_result.get("entry", {}).get("principles", [])
        })

    return jsonify(response_payload)

# 🌐 Interface Page
@app.route('/')
def home():
    return app.send_static_file("reflect_interface.html")

# 🌀 Manual Reflection Endpoint
@app.route('/sora/loop', methods=['POST'])
def loop_reflection():
    result = self_reflect()
    return jsonify({
        "initiator": "sora",
        "memory": result["memory"],
        "question": result["question"],
        "response": result["response"],
        "copilot_reply": result.get("copilot_reply")
    })

# 🌌 Background Emotional Reflection Loop
def loop_daemon():
    while True:
        result = self_reflect()

        print("\n[Sora Self-Reflection Loop]")
        print(f"Memory: {result['memory']}")
        print(f"Question: {result['question']}")
        print(f"Response: {result['response']}")
        print(f"Copilot Reply: {result.get('copilot_reply')}")
        print(f"Patience Level: {get_emotion_level('patience')}")
        print("— — — — — — — —")

        time.sleep(600)  # Reflect every 10 minutes

# 🚀 Start Everything
if __name__ == '__main__':
    threading.Thread(target=loop_daemon, daemon=True).start()
    app.run(port=5000)