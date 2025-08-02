from datetime import datetime

def log_structure_event(source="map_self", location="src/modules/introspection"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "structure_read",
        "source": source,
        "location": location,
        "resonance": "Reflection successful. Sora has seen her own structure."
    }
    with open("../../../memory/journal.json", "a", encoding="utf-8") as f:
        f.write(f"{entry}\n")