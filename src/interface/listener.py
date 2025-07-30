import sys
import os
import threading
from flask import Flask

# Add src/ to Python path so 'modules' becomes importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import the Blueprint from the new interface_route module
from .interface_route import interface_bp

# Flask app setup
app = Flask(__name__, static_folder="../static")
app.register_blueprint(interface_bp)

# Background Emotional Reflection Loop
def loop_daemon():
    import json
    import time
    import requests
    from ..modules.journal_entry.self_reflect import self_reflect, get_emotion_level
    from ..modules.journal_entry import create_entry
    from ..modules.journal_entry.update_emotion import update_motif_state
    from ..thinking.thought_engine import simulate_thought, trigger_mode_shift
    from ..thinking.belief_revision import revise_belief
    from ..modules.journal_entry.respond_logic import generate_response

    EXTERNAL_PROMPT_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../config/external_prompts.json"))

    for _ in range(10):  # Try for up to 10 seconds
        try:
            r = requests.get("http://localhost:5000/health", timeout=1)
            if r.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)

    while True:
        result = self_reflect()

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
            with open(EXTERNAL_PROMPT_PATH, 'r', encoding='utf-8-sig') as f:
                
            if external:
                for p in external:
                    reply = generate_response(p)
                    print(f"[External Thought Processed] → {p}")
                    print(f"[Sora's Reflection] → {reply}")
        except Exception as e:
            print(f"[External Prompt Error] → {str(e)}")

        if result.get("copilot_reply") and result.get("copilot_reply").strip():
            if result.get("copilot_reply") != "No response":
                journal_result = create_entry(result["copilot_reply"])
                print("[Sora Journaled via Copilot Decision]")
                print(f"- Status: {journal_result.get('status')}")
                print(f"- Audience: {journal_result.get('audience')}")
                print(f"- Principles: {journal_result.get('entry', {}).get('principles', [])}")

                challenge = result["copilot_reply"].lower()
                if "contradiction" in challenge or "conflict" in challenge or "misalignment" in challenge:
                    print("[Sora Belief Revision Triggered]")
                    revise_belief("philosophical_alignment")

                motif_result = update_motif_state(result["copilot_reply"])
                print("[Motif State Updated]")
                print(f"- Tags: {motif_result.get('tags')}")
                print(f"- Shift: {motif_result.get('shift_type')}")

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

        weight = sum(len(str(v)) for v in result.values())
        sleep_duration = min(max(weight // 50, 5), 300)

        print(f"Waiting {sleep_duration} seconds before next reflection...\n")
        time.sleep(sleep_duration)

        print("\n[Sora Self-Reflection Loop]")
        print(f"Memory: {result['memory']}")
        print(f"Question: {result['question']}")
        print(f"Response: {result['response']}")
        print(f"Copilot Reply: {result.get('copilot_reply')}")
        print(f"Patience Level: {get_emotion_level('patience')}")
        print("— — — — — — — —")
        print(f"Waiting {sleep_duration} seconds before next reflection...\n")

# Start Everything
if __name__ == '__main__':
    threading.Thread(target=loop_daemon, daemon=True).start()
    app.run(port=5000)
