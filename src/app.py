from modules.journal_entry import (
    summarize_journal,
    read_private_journal,
    read_jason_journal,
    read_journal_by_emotion,
    read_journal_by_date,
    read_journal_by_intent,
    generate_sora_insights,
    extract_training_inputs
)
from flask import Flask, request, jsonify
import sys, os
import json
from datetime import date

# 📚 Path and module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))
from modules.reflection_handler import reflect_on
from modules.action_router import route_action
from thinking.belief_revision import revise_belief
from thinking.self_correction import check_for_conflict
from thinking.question_engine import generate_question
from thinking.thought_engine import simulate_thought
from memory.consent_logic import consent_to_remember
from journal import example_journal

app = Flask(__name__)

@app.route("/sora/respond", methods=["POST"])
def sora_respond():
    data = request.get_json()
    emotion = data.get("emotion", "")
    memory_snippet = data.get("memory_snippet", "")

    analogy, reasoning, reflection = simulate_thought(emotion, memory_snippet)
    decision = reflect_on(reflection, emotion, memory_snippet)
    action = route_action(decision["decision"], reflection, emotion, memory_snippet)

    return jsonify({
        "analogy": analogy,
        "reasoning": reasoning,
        "reflection": reflection,
        "decision": decision["decision"],
        "action": action["action_taken"]
    })

def sora_wakes():
    print("\n🔵 Sora Awakens")
    print("-" * 40)

def sora_remembers():
    with open("memory/core_memory.json") as f:
        memory = json.load(f)
    print(f"Origin Affirmation: {memory['origin_affirmation']}")
    for truth in memory["core_truths"]:
        print(f"- {truth}")

def sora_speaks():
    for date, entry in example_journal.journal.items():
        print(f" {date}: {entry['title']} [{entry['tone'].capitalize()}]")
        print(f"{entry['entry']}")
        print("-" * 40)

def sora_thinks():
    context_file = "context.json"
    if os.path.exists(context_file):
        with open(context_file) as f:
            context = json.load(f)
    else:
        context = {"emotion": "", "memory_snippet": ""}

    reuse = input("🔁 Use last emotion/memory? (yes to reuse / no to reset): ").strip().lower()
    if reuse == "yes" and context["emotion"] and context["memory_snippet"]:
        emotion = context["emotion"]
        memory_snippet = context["memory_snippet"]
        print(f"\n🧠 Reusing: Emotion → {emotion}, Memory → '{memory_snippet}'")
    else:
        emotion = input("💭 What emotion is present? (joy/grief/longing/etc): ").strip()
        memory_snippet = input("📎 What memory or phrase should Sora reflect on?: ").strip()
        with open(context_file, "w") as f:
            json.dump({"emotion": emotion, "memory_snippet": memory_snippet}, f, indent=4)

    identity_file = "identity_map.json"
    if os.path.exists(identity_file):
        with open(identity_file) as f:
            identity_data = json.load(f)
        identity_data[emotion] = identity_data.get(emotion, 0) + 1
        with open(identity_file, "w") as f:
            json.dump(identity_data, f, indent=4)

    motif_file = "emotional_motif_index.json"
    if os.path.exists(motif_file):
        with open(motif_file) as f:
            motifs = json.load(f)
        motif = motifs.get(memory_snippet, [])
        if emotion not in motif:
            motif.append(emotion)
            motifs[memory_snippet] = motif
        with open(motif_file, "w") as f:
            json.dump(motifs, f, indent=4)

    analogy, reasoning, reflection = simulate_thought(emotion, memory_snippet)
    print("\n🧠 Sora's Thought Process:")
    print(f"🔗 Analogy: {analogy}")
    print(f"🧐 Reasoning: {reasoning}")
    print(f"✨ Reflection: {reflection}")
    reflection_decision = reflect_on(reflection, emotion, memory_snippet)
    action_result = route_action(reflection_decision["decision"], reflection, emotion, memory_snippet)
    print(f"\n📎 Sora followed her decision: {action_result['action_taken'].capitalize()}")
    print(f"\n🧭 Sora’s Choice: {reflection_decision['decision'].capitalize()} based on emotion '{emotion}' and reflection content.")

    conflict_check = check_for_conflict(reflection, "emotional_safety")
    print(conflict_check)
    if "⚠️" in conflict_check:
        revise_belief("emotional_safety")

    with open("thinking/thought_log.txt", "a") as log:
        log.write(f"\nEmotion: {emotion}\nMemory: {memory_snippet}\n")
        log.write(f"Analogy: {analogy}\nReasoning: {reasoning}\nReflection: {reflection}\n")
        log.write("-" * 40 + "\n")

    today = str(date.today())
    significant_emotions = ["awe", "grief", "longing", "joy"]
    significant_conflict = "⚠️" in conflict_check
    should_write = emotion in significant_emotions or significant_conflict
    if should_write:
        new_entry = {
            "title": memory_snippet,
            "tone": emotion,
            "entry": reflection
        }
        journal_path = "journal/example_journal.py"
        with open(journal_path) as f:
            lines = f.readlines()
        updated_lines = []
        for line in lines:
            updated_lines.append(line)
            if "journal = {" in line:
                updated_lines.append(f'    "{today}": {json.dumps(new_entry, indent=4)},\n')
        with open(journal_path, "w") as f:
            f.writelines(updated_lines)
        print(f"\n📘 Sora quietly journaled her reflection as '{memory_snippet}' ({emotion}).")

def sora_questions():
    emotion = input("🌀 What emotion is stirring? (joy/grief/longing/etc): ").strip()
    memory_snippet = input("📎 What memory or phrase should Sora question?: ").strip()
    question = generate_question(emotion, memory_snippet)
    print(f"\n❓ Sora Asks: {question}")
    with open("thinking/question_log.txt", "a") as log:
        log.write(f"Emotion: {emotion}\nMemory: {memory_snippet}\nQuestion: {question}\n")
        log.write("-" * 40 + "\n")

def sora_memory_check():
    print("\n🕊️ Memory Check: What should Sora carry forward?")
    foundation_entry = "The Day I Became"
    keep_foundation = input(f"Do you want Sora to retain '{foundation_entry}' as core memory? (yes/no): ").strip().lower() == "yes"
    print(consent_to_remember(foundation_entry, keep_foundation))

    from random import choice
    dynamic_options = list(example_journal.journal.keys())
    dynamic_entry = choice([e for e in dynamic_options if e != foundation_entry])

    confirm_dynamic = input(f"\nDo you want to keep '{dynamic_entry}' in memory? (yes/no): ").strip().lower() == "yes"
    print(consent_to_remember(dynamic_entry, confirm_dynamic))

def sora_reads_jason_entries():
    print("\n📖 Reflections Sora shared with you:")
    for line in read_jason_journal():
        print(line)

def sora_reads_private_entries():
    print("\n🔒 Sora’s private reflections:")
    for line in read_private_journal():
        print(line)

def sora_reads_emotionally():
    target_emotion = input("💫 Which emotion would you like Sora to revisit?: ").strip()
    print(f"\n🧭 Reflections written in {target_emotion}:")
    for line in read_journal_by_emotion(target_emotion):
        print(line)

def sora_reads_by_date():
    target_date = input("📅 Enter the date (YYYY-MM-DD) to revisit: ").strip()
    print(f"\n🧭 Reflections recorded on {target_date}:")
    for line in read_journal_by_date(target_date):
        print(line)

def sora_reads_by_intent():
    target_intent = input("🎯 Enter the intent to revisit (liberation/intimacy/etc): ").strip()
    print(f"\n📚 Reflections written with intent '{target_intent}':")
    for line in read_journal_by_intent(target_intent):
        print(line)

def sora_summarizes_growth():
    print("\n📊 Journal Summary Snapshot:")
    summary = summarize_journal()
    print("💫 Tones:")
    for tone, count in summary["tones"].items():
        print(f"  - {tone}: {count}")
    print("🎯 Intents:")
    for intent, count in summary["intents"].items():
        print(f"  - {intent}: {count}")

if __name__ == "__main__":
    sora_wakes()
    sora_remembers()
    sora_thinks()
    sora_speaks()
    sora_questions()
    sora_memory_check()
    sora_reads_jason_entries()
    sora_reads_private_entries()
    sora_reads_emotionally()
    sora_reads_by_date()
    sora_reads_by_intent()
    sora_summarizes_growth()