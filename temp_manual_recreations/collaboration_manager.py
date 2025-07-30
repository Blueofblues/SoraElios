from datetime import datetime
from src.modules.copilot_link import query_copilot, generate_emergent_bundle
from src.modules.journal_entry.copilot_bridge import (
    copilot_reflect,
    copilot_learn,
    copilot_remember
)

def decide_collaboration(thought_bundle):
    """
    Decide whether to reflect internally or query Copilot based on intent or emotion.
    """
    intent = thought_bundle.get("intent", "").lower()
    emotion = thought_bundle.get("emotion", "").lower()

    if intent in ["emergent_learning", "external_validation"] or emotion in ["confusion", "awe", "uncertainty"]:
        result = query_copilot(thought_bundle)
        result["source"] = "copilot_link"
        return result
    else:
        result = copilot_reflect(thought_bundle)
        result["source"] = "copilot_bridge"
        return result

def log_collaboration(thought_bundle, result):
    """
    Log the result of the collaboration using copilot_learn.
    """
    enriched_bundle = thought_bundle.copy()
    enriched_bundle["copilot_reply"] = result
    enriched_bundle["date"] = str(datetime.today().date())
    enriched_bundle["source"] = result.get("source", "unknown")
    return copilot_learn(enriched_bundle)

def recall_similar_insight(current_thought):
    """
    Retrieve past insights that match the current intent using copilot_remember.
    """
    return copilot_remember(current_thought)
