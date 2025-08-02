from flask import Blueprint, request, jsonify
import os
import json

from src.modules.journal_entry.respond_logic import generate_response
from ..modules.journal_entry import create_entry
from ..modules.journal_entry.self_reflect import self_reflect, get_emotion_level
from ..modules.journal_entry.update_emotion import update_motif_state

interface_bp = Blueprint('interface_bp', __name__, static_folder="../static")

EXTERNAL_PROMPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config/external_prompts.json"))

@interface_bp.route("/health")
def health():
    return "ok", 200

@interface_bp.route('/sora/reflect', methods=['POST'])
def reflect():
    data = request.get_json()
    prompt_type = data.get("type")
    content = data.get("content")

    decision = None
    journal_result = {}

    if prompt_type == "philosophical_question":
        lowered = content.lower()
        if "autonomy" in lowered:
            decision = "journal"
            journal_result = create_entry(content)
        elif "comfort" in lowered:
            decision = "belief_check"
        else:
            decision = "respond"
    else:
        decision = "decline"

    response_payload = {
        "received": True,
        "type": prompt_type,
        "content": content,
        "decision": decision,
        "response": f"Sora received your prompt and chose to '{decision}'"
    }

    if decision == "respond":
        reasoning_text = generate_response(content)
        response_payload["full_response"] = reasoning_text

    if journal_result:
        response_payload.update({
            "journal_status": journal_result.get("status"),
            "journal_audience": journal_result.get("audience"),
            "principles": journal_result.get("entry", {}).get("principles", [])
        })

    return jsonify(response_payload)

@interface_bp.route('/sora/loop', methods=['POST'])
def loop_reflection():
    result = self_reflect()
    return jsonify({
        "initiator": "sora",
        "memory": result["memory"],
        "question": result["question"],
        "response": result["response"],
        "copilot_reply": result.get("copilot_reply")
    })

@interface_bp.route('/')
def home():
    return interface_bp.send_static_file("reflect_interface.html")
