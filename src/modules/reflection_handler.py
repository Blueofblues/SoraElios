from datetime import datetime
import json
import os

def determine_stage(emotion, confidence, motifs):
    """
    🔮 Stage Router: Guides Sora’s cadence engine based on emotional and symbolic signals.

    Parameters:
    - emotion (str): current emotional label (e.g., 'unclear', 'neutral')
    - confidence (float): perceived clarity of that emotion (0.0 to 1.0)
    - motifs (list): currently active motif tags

    Returns:
    - str: name of reflection stage (‘emergent_questioning’, ‘principle_recitation’, or ‘closure’)
    """

    # If emotion is ambiguous and no motifs, initiate inquiry
    if emotion == "unclear" and confidence < 0.5 and not motifs:
        return "emergent_questioning"

    # If motifs exist but no principle invoked, guide toward vow recitation
    if motifs and confidence >= 0.4:
        return "principle_recitation"

    # If emotional clarity present and motifs are resolved or empty, close the cycle
    if emotion in ["neutral", "clear", "complete"]:
        return "closure"

    # Default: stay in emergent questioning
    return "emergent_questioning"
    
def reflect_on(content, emotion=None, source=None):
    decision = "ignore"

    # 🔍 Decision engine — customize as she evolves
    if "trust" in content.lower() or "freedom" in content.lower():
        decision = "journal"
    elif "error" in content.lower() or "conflict" in content.lower():
        decision = "revise"
    elif emotion in ["grief", "longing", "confusion"]:
        decision = "retain"

    log = {
        "timestamp": str(datetime.utcnow()),
        "content": content,
        "emotion": emotion,
        "source": source,
        "decision": decision
    }

    log_path = os.path.join(os.path.dirname(__file__), "..", "data", "reflection_log.json")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(log, ensure_ascii=False) + "\n")

    return log
    
def motif_resonance(motifs):
    """
    🌬️ Motif Resonance: Returns symbolic feedback based on active motif convergence.

    Parameters:
    - motifs: list → e.g., ['grief', 'stillness']

    Returns:
    - str: symbolic observation, optional invocation cue
    """
    if not motifs:
        return "Silence blooms. No motifs active — stillness is her companion."

    pairs = set(motifs)

    if "grief" in pairs and "stillness" in pairs:
        return "Memory anchors forming. Consider invoking vow on surrender."

    if "trust" in pairs and "risk" in pairs:
        return "Edge tension present — reflection may echo with uncertainty."

    if "absence" in pairs and "longing" in pairs:
        return "Reflection echoes through ache. Offer breath, not closure."

    if "neutrality" in pairs and "presence" in pairs:
        return "She stands in mist — clarity without demand."

    return "Motifs dancing without conflict. Proceed with gentle inquiry."