import json

def revise_belief(belief_key):
    with open("beliefs.json") as f:
        beliefs = json.load(f)
    
    current_belief = beliefs.get(belief_key, "No belief found.")
    print(f"\n🧭 Current belief: '{belief_key}' → {current_belief}")

    revise = input("Do you want to revise this belief? (yes/no): ").strip().lower()
    if revise == "yes":
        new_belief = input("Enter the revised belief: ").strip()
        beliefs[belief_key] = new_belief

        with open("beliefs.json", "w") as f:
            json.dump(beliefs, f, indent=4)

        # Log change
        with open("thinking/belief_change_log.txt", "a") as log:
            log.write(f"\nRevised belief: '{belief_key}'\nOld: {current_belief}\nNew: {new_belief}\n")
            log.write("-" * 40 + "\n")

        print("✅ Belief updated and logged.")
    else:
        print("🕊️ Belief remains unchanged.")
