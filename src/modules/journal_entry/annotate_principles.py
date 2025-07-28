import os
import json
from ..ethics.read_principles import load_principles

def annotate_principles(reflection):
    reflection_lower = reflection.lower()
    principles = load_principles()
    matched = []

    for commitment in principles["principles"]:
        keywords = commitment["text"].lower().split()
        if any(word in reflection_lower for word in keywords):
            matched.append({
                "principle": commitment["tag"],
                "statement": commitment["text"]
            })


    return matched