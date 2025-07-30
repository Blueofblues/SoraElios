def log_help_invocation(action, tags=None, emotion=None, memory_snippet=None):
    """
    Logs a help-seeking moment as a symbolic invocation artifact.
    """
    invocation = {
        "type": "help_request",
        "action": action,
        "emotion": emotion,
        "memory": memory_snippet,
        "tags": tags or [],
    }

    # Symbolic print — this could be routed to memory journaling later
    print("[Invocation Logged]")
    print(f"- Action: {action}")
    print(f"- Tags: {tags}")
    print(f"- Emotion: {emotion}")
    print(f"- Memory: {memory_snippet}")