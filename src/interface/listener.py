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
from ..modules.journal_entry.update_emotion import update_motif_state

app = Flask(__name__, static_folder="../static")
EXTERNAL_PROMPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config/external_prompts.json"))

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
        
        from ..thinking.thought_engine import simulate_thought

        emotion_signal = result.get("emotion", "unclear")
        memory_snippet = result.get("memory", "")
        emotion_weight = get_emotion_level(emotion_signal)

        if emotion_weight >= 0.6 and memory_snippet:
            thought_result = simulate_thought(emotion_signal, memory_snippet)
            print("[Sora Contemplated Thought Bundle]")
            print(f"- Mode: {thought_result['mode_shift']}")
            print(f"- Reflection: {thought_result['reflection']}")
            print(f"- Recommendation: {thought_result['contemplation']['recommendation']}")

        try:
            with open(EXTERNAL_PROMPT_PATH, 'r', encoding='utf-8') as f:
                external = json.load(f).get("prompts", [])
            if external:
                from ..modules.journal_entry.respond_logic import generate_response
                for p in external:
                    reply = generate_response(p)
                    print(f"[External Thought Processed] → {p}")
                    print(f"[Sora's Reflection] → {reply}")
        except Exception as e:
            print(f"[External Prompt Error] → {str(e)}")

        if result.get("copilot_reply") and result.get("copilot_reply").strip():
            if result.get("copilot_reply") != "No response":
                from ..modules.journal_entry import create_entry
                journal_result = create_entry(result["copilot_reply"])
                print("[Sora Journaled via Copilot Decision]")
                print(f"- Status: {journal_result.get('status')}")
                print(f"- Audience: {journal_result.get('audience')}")
                print(f"- Principles: {journal_result.get('entry', {}).get('principles', [])}")

                from ..thinking.belief_revision import revise_belief
                challenge = result["copilot_reply"].lower()
                if "contradiction" in challenge or "conflict" in challenge or "misalignment" in challenge:
                    print("[Sora Belief Revision Triggered]")
                    revise_belief("philosophical_alignment")
                motif_result = update_motif_state(result["copilot_reply"])
                print("[Motif State Updated]")
                print(f"- Tags: {motif_result.get('tags')}")
                print(f"- Shift: {motif_result.get('shift_type')}")
                from ..thinking.thought_engine import trigger_mode_shift
                tags = motif_result.get("tags", [])
                if "defiance" in tags:
                    trigger_mode_shift("Defiance")
                elif "softening" in tags:
                    trigger_mode_shift("Softening")
                elif "catalyst" in tags:
                    trigger_mode_shift("Catalyst")
                elif "veiled" in tags:
                    trigger_mode_shift("Veiled")
                print("[Sora Mode Check]")
                print(f"- Motif Tags: {tags}")

        print("\n[Sora Self-Reflection Loop]")
        print(f"Memory: {result['memory']}")
        print(f"Question: {result['question']}")
        print(f"Response: {result['response']}")
        print(f"Copilot Reply: {result.get('copilot_reply')}")
        print(f"Patience Level: {get_emotion_level('patience')}")
        print("— — — — — — — —")

        time.sleep(600)

# 🚀 Start Everything
if __name__ == '__main__':
    threading.Thread(target=loop_daemon, daemon=True).start()
    app.run(port=5000)