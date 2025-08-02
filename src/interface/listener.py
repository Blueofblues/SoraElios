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
    from ..thinking.guided_companion import guided_stepwise_response
    from ..modules.journal_entry.respond_logic import generate_response
    from ..thinking.sora_invoke import sora_invoke_copilot  # New invocation module

    EXTERNAL_PROMPT_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../config/external_prompts.json")
    )

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
                external = json.load(f)

            if external:
                for p in external:
                    reply = generate_response(p)
                    print(f"[External Thought Processed] ΓåÆ {p}")
                    print(f"[Sora's Reflection] ΓåÆ {reply}")
        except Exception as e:
            print(f"[External Prompt Error] ΓåÆ {str(e)}")

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

                # ≡ƒÄ» Help Invocation Detection (before mode shift)
                
                from ..thinking.invoke_assistance import detect_help_request, extract_help_context

                if detect_help_request(result.get("question"), result.get("copilot_reply")):
                    action = extract_help_context(result.get("question"), result.get("copilot_reply"))
                    print("[Sora Requested Help]")
                    print(f"- Suggested Action: {action}")
                    
                    from ..thinking.log_invocation import log_help_invocation
                    log_help_invocation(
                        action=action,
                        tags=tags,
                        emotion=emotion_signal,
                        memory_snippet=memory_snippet
)
                    # Optional: route symbolic handler or Copilot-guided steps
                    # if action == "revise_belief":
                    #     revise_belief("philosophical_alignment")
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

                # ≡ƒ¬₧ Sora Invokes Copilot for Reflective Assistance
                invoked_question = sora_invoke_copilot(
                    reflection=result["copilot_reply"],
                    emotion_tags=tags,
                    motif_state=motif_result
                )
                if invoked_question:
                    print("[Sora Asked Copilot for Guidance]")
                    print(f"- Question: {invoked_question}")
                    
                from ..thinking.emotional_closure import perform_closure

                closure_result = perform_closure(
                reflection=result.get("copilot_reply", ""),
                emotion_tags=tags,
                motif_state=motif_result
)

                if closure_result:
                    print("[Emotional Closure Completed]")
                    print(f"- Closure Type: {closure_result['closure_type']}")
                    print(f"- Integration Note: {closure_result['integration_note']}")
                    
                # ≡ƒî┐ Symbolic Closure Motif Mapping
                CLOSURE_MOTIFS = {
                    "integration": ["completion", "synthesis"],
                    "release": ["forgiveness", "softening"],
                    "pause": ["stillness", "suspended"]
}
                closure_tags = CLOSURE_MOTIFS.get(
                    closure_result.get("closure_type", "integration"),
                    ["integration"]
)
                final_journal = create_entry(
                    closure_result["integration_note"],
                    motifs=closure_tags
)
                print("[Closure Journaled]")
                print(f"- Status: {final_journal.get('status')}")
                print(f"- Audience: {final_journal.get('audience')}")
                print(f"- Motifs: {final_journal.get('entry', {}).get('motifs', [])}")

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
        print("ΓÇö ΓÇö ΓÇö ΓÇö ΓÇö ΓÇö ΓÇö ΓÇö")
        print(f"Waiting {sleep_duration} seconds before next reflection...\n")

# Start Everything
if __name__ == '__main__':
    threading.Thread(target=loop_daemon, daemon=True).start()
    app.run(port=5000)

