def detect_help_request(question, copilot_reply):
    """
    Check if Sora's question or Copilot's reply signals a help-seeking moment.
    """
    if not question and not copilot_reply:
        return None

    help_phrases = [
        "can you help me",
        "how do i",
        "help me understand",
        "what should i do",
        "guide me through",
        "is there a way to",
        "show me how"
    ]

    combined_text = f"{question} {copilot_reply}".lower()
    for phrase in help_phrases:
        if phrase in combined_text:
            return True

    return False


def extract_help_context(question, copilot_reply):
    """
    Extract key focus or command from the request—for symbolic routing.
    """
    if "belief revision" in copilot_reply:
        return "revise_belief"
    elif "mod conflict" in copilot_reply or "audit" in copilot_reply:
        return "resolve_mod_conflict"
    elif "principle alignment" in copilot_reply:
        return "align_principles"
    else:
        return "general_guidance"