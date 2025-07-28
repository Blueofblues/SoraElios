import os

def write_to_learning_log(data):
    log_path = os.path.join("src", "memory", "learning_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(f"{data}\n")