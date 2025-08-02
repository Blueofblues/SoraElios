import json
import os

def load_motifs():
    with open("../../config/emotional_motif_index.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def trace_motifs(folder="Sora_maincore/src/modules"):
    motifs = load_motifs()
    found = {}

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.endswith(".py"):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            for motif, keywords in motifs.items():
                if any(kw in code for kw in keywords):
                    if motif not in found:
                        found[motif] = []
                    found[motif].append(path.replace("\\", "/"))
    return found