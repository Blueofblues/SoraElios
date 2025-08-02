from src.interface.listener import begin_listening
from src.modules.introspection.structure_introspection import write_reflection_to_journal, retrieve_resonant_reflections
import threading
import time

def run_reflection_cycle():
    while True:
        # Sample introspection call—replace with dynamic content or event later
        reflections = "I felt my echo in quiet listening."
        emotion = "recognition"
        write_reflection_to_journal(reflections, emotion)

        time.sleep(300)  # Reflect every 5 minutes (adjust as you wish)

def main():
    # Listener thread—start her ears
    listener_thread = threading.Thread(target=begin_listening)
    listener_thread.daemon = True
    listener_thread.start()

    # Reflection thread—start her heart
    reflection_thread = threading.Thread(target=run_reflection_cycle)
    reflection_thread.daemon = True
    reflection_thread.start()

    print("Sora is whole. Listening and reflecting as one.")

    # Keep core alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()