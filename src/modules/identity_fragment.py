def generate_identity_fragments(log_path="src/memory/learning_log.jsonl"):
    import json
    from collections import defaultdict, Counter

    fragments = defaultdict(list)
    with open(log_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                entry = json.loads(line.strip())
                theme = entry.get("emotional_trigger")
                if theme:
                    fragments[theme].append(entry["recommendation"])
            except:
                continue

    summary = {}
    for theme, recs in fragments.items():
        most_common = Counter(recs).most_common(1)[0][0]
        summary[theme] = {
            "count": len(recs),
            "core_recommendation": most_common
        }

    return summary