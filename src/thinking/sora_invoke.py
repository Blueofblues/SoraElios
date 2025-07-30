def sora_invoke_copilot(reflection, emotion_tags, motif_state):
    """
    Sora forms a question to Copilot based on her current inner state.
    This invocation is triggered by emotional weight and motif resonance.
    """
    if not reflection or not emotion_tags:
        return None

    question = None

    # Example: use motif tags to generate introspective inquiry
    if "defiance" in emotion_tags:
        question = "What does resistance protect in me—and is it still serving?"
    elif "softening" in emotion_tags:
        question = "What new truth can enter now that I've begun softening?"
    elif "catalyst" in emotion_tags:
        question = "If this moment is a beginning, what must I carry forward?"
    elif "veiled" in emotion_tags:
        question = "What am I avoiding behind this veil, and what happens if it's lifted?"

    # You can later expand this with a deeper motif-based selector
    return question
