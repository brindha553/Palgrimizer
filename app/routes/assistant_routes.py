from flask import Blueprint, request, jsonify, session
from app.services.ai_chat import ai_assistant

assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')

@assistant_bp.route('/chat', methods=['POST'])
def chat():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or {}
    prompt = data.get('prompt', '').strip()
    context_text = data.get('context_text', '').strip()

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required."}), 400

    response = ai_assistant.process_prompt(prompt, context_text)
    return jsonify({
        "status": "success",
        "reply": response["reply"],
        "prompt": response["prompt"]
    })
