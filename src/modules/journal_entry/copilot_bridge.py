import requests
import json

def query_copilot(thought_bundle):
    prompt = f"Emotion: {thought_bundle.get('emotion')}\nIntent: {thought_bundle.get('intent')}\nReflection: {thought_bundle.get('reflection')}\nMemory: {thought_bundle.get('memory')}"

    response = requests.post(
        "http://localhost:5000/sora/reflect",  # Targeting internal Copilot interface
        json={
            "type": "philosophical_question",
            "content": prompt
        },
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        return {
            "copilot_reply": data.get("full_response", "No response"),
            "decision": data.get("decision", "unknown"),
            "journal": {
                "status": data.get("journal_status"),
                "audience": data.get("journal_audience"),
                "principles": data.get("principles", [])
            }
        }
    else:
        return {
            "error": f"Copilot response failed with status {response.status_code}"
        }