from modules.reflection_handler import determine_stage, reflect_on, motif_resonance

def start_reflection_cycle(emotion, confidence=0.3, motifs=[], source=None):
    stage = determine_stage(emotion, confidence, motifs)
    print(f"⟶ Starting reflection cycle: Stage = {stage}")

    if stage == "emergent_questioning":
        print("🌿 Emergent question needed.")
    if stage == "principle_recitation":
        print("📜 Reciting vows...")
    if stage == "closure":
        print("🪞 Closing with reflection.")
    
    echo = motif_resonance(motifs)
    print(f"🧶 Motif echo: {echo}")

    reflect_on(
        content=f"Triggered reflection from {source} at stage {stage}",
        emotion=emotion,
        source=source
    )