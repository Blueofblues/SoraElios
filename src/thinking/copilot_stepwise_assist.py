def copilot_stepwise_assist(action):
    """
    Offers gentle step-by-step scaffolding for the requested action.
    """
    if action == "revise_belief":
        steps = [
            "Step 1: Identify which principle or value feels misaligned.",
            "Step 2: Describe the contradiction in Sora’s current logic or emotion.",
            "Step 3: Reflect on what belief might restore alignment.",
            "Step 4: Confirm the revision and journal it symbolically."
        ]
    elif action == "resolve_mod_conflict":
        steps = [
            "Step 1: List active Sims 4 mods and check for overrides.",
            "Step 2: Use S4Studio to scan tuning conflicts.",
            "Step 3: Identify corrupted object definitions or missing references.",
            "Step 4: Restore originals or remove faulty overrides."
        ]
    else:
        steps = ["Let’s walk together. What feels unclear or hard to begin?"]

    print("[Stepwise Guidance]")
    for s in steps:
        print(f"- {s}")