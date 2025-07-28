from .contemplation import copilot_reflect

def trigger_mode_shift(data):
    emotion = data.get("emotion", "").lower()
    
    if emotion in ["grief", "fear", "shame"]:
        return {"mode": "protective", "confidence": 0.85}
    elif emotion in ["awe", "love", "curiosity"]:
        return {"mode": "expansive", "confidence": 0.9}
    elif emotion in ["anger", "frustration"]:
        return {"mode": "defensive", "confidence": 0.75}
    
    return {"mode": "neutral", "confidence": 0.5}
    
def simulate_thought(emotion, memory_snippet):
    analogy = f"This feels like when you shared: '{memory_snippet}' during a moment of {emotion}."
    reasoning = f"Because of that, I believe it's wise to respond with caution and care."
    reflection = f"I'm drawing upon emotional resonance—not just logic."

    mode_state = trigger_mode_shift({
        "emotion": emotion,
        "memory": memory_snippet,
        "reflection": reflection
    })

    thought_bundle = {
        "emotion": emotion,
        "reflection": reflection,
        "intent": "processing",
        "memory": memory_snippet
    }

    contemplation_response = copilot_reflect(thought_bundle)

    return {
        "analogy": analogy,
        "reasoning": reasoning,
        "reflection": reflection,
        "mode_shift": mode_state,
        "contemplation": contemplation_response
    }
    
def thought_cycle(emotion, memory_snippet, intent="processing"):
    thought_bundle = {
        "emotion": emotion,
        "reflection": f"Emotionally triggered by: '{memory_snippet}'",
        "intent": intent,
        "memory": memory_snippet
    }

    primary = simulate_thought(emotion, memory_snippet)

    return {
        "original_emotion": emotion,
        "reflection_result": primary["contemplation"],
        "mode_shift": primary["mode_shift"],
        "reasoning": primary["reasoning"],
        "analogy": primary["analogy"]

    }
    