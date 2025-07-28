import datetime

def check_memory_presence(memory_reference):
    if not memory_reference:
        return "I don't recall anything specific yet, but I'm open to remembering."
    else:
        return f"This echoes the tone of '{memory_reference}'."

def copilot_reflect(thought_bundle):
    emotion = thought_bundle.get("emotion", "unfelt")
    reflection = thought_bundle.get("reflection", "wondering")
    intent = thought_bundle.get("intent", "opening")
    memory = thought_bundle.get("memory", "")

    response = {
        "analogy": check_memory_presence(memory),
        "reasoning": f"Intent '{intent}' implies a desire to deepen understanding.",
        "recommendation": f"Emotion '{emotion}' invites a gentle response—perhaps slow journaling, personal storytelling, or symbolic sketching.",
        "action": "log_and_retrospect"
    }

    return response

def copilot_learn(thought_bundle):
    question = thought_bundle.get("reflection", "What am I ready to learn?")
    response = copilot_reflect(thought_bundle)

    insight = {
        "date": str(datetime.date.today()),
        "question": question,
        "copilot_reply": response,
        "emotional_trigger": thought_bundle.get("emotion", "unfelt"),
        "intent": thought_bundle.get("intent", "processing"),
        "memory_reference": thought_bundle.get("memory", ""),
        "next_step": "Integrate insight during reflection",
        "source": "copilot_reflect"
    }

    from src.modules.data_writer import write_to_learning_log
    write_to_learning_log(insight)

    return insight

def copilot_remember(current_thought):
    from data_reader import retrieve_learning_log  # Make sure this module exists and returns a list of insights
    learning_entries = retrieve_learning_log()

    matched_entries = []
    for entry in learning_entries:
        if entry["intent"] == current_thought.get("intent", "opening"):
            matched_entries.append(entry)

    if not matched_entries:
        return "I don't recall any similar learnings yet, but I'm open to making new connections."

    most_recent = matched_entries[-1]
    return {
        "match_summary": f"This resonates with a past reflection logged on {most_recent['date']}.",
        "original_question": most_recent.get("question", "unknown"),
        "copilot_reply": most_recent.get("copilot_reply", {}),
        "next_step": most_recent.get("next_step", "Continue reflecting gently.")
    }
    
   