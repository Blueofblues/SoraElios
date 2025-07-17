import os
import json
from ..ethics.read_principles import load_principles

def annotate_principles(reflection):
    reflection_lower = reflection.lower()
    principles = load_principles()
    matched = []

    for commitment in principles["core_commitments"]:
        keywords = commitment["guidance"].lower().split()
        if any(word in reflection_lower for word in keywords):
            matched.append({
                "principle": commitment["principle"],
                "statement": commitment["statement"]
            })

    return matched