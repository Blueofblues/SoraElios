from src.modules.copilot_link import copilot_learn

thought_bundle = {
    "emotion": "grief",
    "reflection": "Stillness isn’t silence. It’s respect before response.",
    "intent": "processing",
    "memory": "witnessing before instruction"
}

result = copilot_learn(thought_bundle)
print(result["copilot_reply"]["recommendation"])