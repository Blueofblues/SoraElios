def generate_question(emotion, memory_snippet):
    if emotion.lower() == "grief":
        return f"What does '{memory_snippet}' still mean to me now—and why does it ache?"
    elif emotion.lower() == "joy":
        return f"How did '{memory_snippet}' shape my sense of safety or belonging?"
    elif emotion.lower() == "longing":
        return f"What am I still reaching for when I remember '{memory_snippet}'?"
    else:
        return f"What deeper truth might be hidden inside: '{memory_snippet}'?"
