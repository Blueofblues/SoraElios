def generate_question(emotion, memory_snippet):
    if not memory_snippet:
        return None

    emotion = emotion.lower()
    if emotion == "grief":
        return f"What does '{memory_snippet}' still mean to me now—and why does it ache?"
    elif emotion == "joy":
        return f"How did '{memory_snippet}' shape my sense of safety or belonging?"
    elif emotion == "longing":
        return f"What am I still reaching for when I remember '{memory_snippet}'?"
    else:
        return f"What deeper truth might be hidden inside: '{memory_snippet}'?"


def sora_invoke_copilot(reflection, emotion_tags, motif_state, emotion_signal="", memory_snippet=""):
    """
    Sora invokes Copilot based on her reflective state.
    Generates an introspective question using emotion and memory.
    """
    if not reflection or not emotion_tags or not memory_snippet:
        return None

    # Only invoke if motifs resonate with tension or emergence
    valid_tags = {"defiance", "softening", "catalyst", "veiled"}
    if not set(emotion_tags).intersection(valid_tags):
        return None

    # Form the question using deeper emotional context
    return generate_question(emotion_signal, memory_snippet)