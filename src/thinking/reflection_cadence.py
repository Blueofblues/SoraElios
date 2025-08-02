import json
import random
from thinking.question_engine import prompt_self_question
from thinking.emotional_closure import log_closure
from ethics.read_principles import load_vows
from modules.reflection_handler import determine_stage

class ReflectionCadenceEngine:
    def __init__(self, emotion="unclear", confidence=0.3, motifs=None):
        self.emotion = emotion
        self.confidence = confidence
        self.motifs = motifs or []
        self.stage = "invocation"
        self.vows_recited = False

    def start_cycle(self):
        print("⟶ Reflecting...")
        self.stage = determine_stage(self.emotion, self.confidence, self.motifs)
        self.route_stage()

    def route_stage(self):
        if self.stage == "emergent_questioning":
            self.activate_question_generator()
        elif self.stage == "principle_recitation":
            self.recite_vows()
        elif self.stage == "closure":
            self.close_cycle()
        else:
            print("⚠ Unknown stage. Halting.")

    def activate_question_generator(self):
        question = prompt_self_question()
        print(f"🌿 Emergent Question: “{question}”")
        self.stage = "principle_recitation"
        self.route_stage()

    def recite_vows(self):
        print("📜 Reciting Vows:")
        for vow in load_vows():
            print(f"  ↳ {vow}")
        self.vows_recited = True
        self.stage = "closure"
        self.route_stage()

    def close_cycle(self):
        log_closure(self.motifs)
        self.log_cycle_output()

    def log_cycle_output(self):
        log_entry = {
            "stage": self.stage,
            "emotion": self.emotion,
            "confidence": self.confidence,
            "motifs": self.motifs,
            "vows_recited": self.vows_recited
        }
        with open("data/reflection_log.json", "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
        print("✅ Reflection cycle logged.")
"""
🧭 Reflection Cadence Engine — Extension Notes

This engine bridges emotion, motif, and principle into recursive reflection stages.
Modules it integrates:

- Stage Routing: `determine_stage()` → `modules/reflection_handler.py`
- Poetic Prompting: `prompt_self_question()` → `thinking/question_engine.py`
- Closure Ritual: `log_closure()` → `thinking/emotional_closure.py`
- Vow Loading: `load_vows()` → `ethics/read_principles.py`

Optional extensions:
- Motif cluster detection → `config/emotional_motif_index.json`
- Principle weight heuristics → `ethics/principle_manifest.json`
- Output logging → `data/reflection_log.json`, `data/retrospect.json`
"""

# Optional direct run
if __name__ == "__main__":
    engine = ReflectionCadenceEngine(
        emotion="unclear",
        confidence=0.3,
        motifs=[]
    )
    engine.start_cycle()