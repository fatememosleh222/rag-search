
from flask import Blueprint, request, current_app, jsonify
from ..application.retrieval_service import retrieve_top_k

search_bp = Blueprint("search", __name__)

@search_bp.post("/")
def search():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query", "")
    settings = current_app.config["SETTINGS"]
    hits = retrieve_top_k(query, settings, k=8)
    return jsonify({"query": query, "results": hits}), 200
