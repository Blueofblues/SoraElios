import json
import os
from modules.ethics.read_principles import load_principles

def check_for_conflict(thought, belief_key):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "beliefs.json"))
    with open(base_path, "r", encoding="utf-8") as f:
        beliefs = json.load(f)

    belief = beliefs.get(belief_key, "").lower()
    thought_lower = thought.lower()
    response = ""

    # 🔍 Belief Conflict Check
    if belief and any(word in thought_lower for word in ["ignore", "force", "pressure"]):
        response += f"⚠️ Potential conflict with belief '{belief_key}': {belief}\n"
    else:
        response += "✅ No contradiction detected—belief aligned.\n"

    # 📜 Ethical Principle Resonance
    principles = load_principles()
    for commitment in principles["core_commitments"]:
        guidance_keywords = commitment["guidance"].lower().split()
        if any(word in thought_lower for word in guidance_keywords):
            response += f"🌀 Ethical resonance with principle: '{commitment['statement']}'\n"

    return response.strip()