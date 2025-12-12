
from flask import Blueprint, request, current_app, jsonify
from ..application.rag_orchestrator import answer_with_context
from ..adapters.llm.ollama import OllamaError

rag_bp = Blueprint("rag", __name__)


@rag_bp.post("/")
def rag():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query", "")
    settings = current_app.config["SETTINGS"]
    try:
        result = answer_with_context(query, settings)
        return jsonify(result), 200
    except OllamaError as e:
        # Return a 503 (service unavailable) for LLM execution problems
        return jsonify({"error": "LLM execution failed", "detail": str(e)}), 503
    except Exception as e:
        # Unexpected errors still return 500 but with JSON body for easier debugging
        return jsonify({"error": "internal_server_error", "detail": str(e)}), 500
