
from typing import Dict, Any
from .retrieval_service import retrieve_top_k
from ..adapters.llm.ollama import generate

SYSTEM = (
    "You are a helpful assistant. Answer ONLY using the provided context. "
    "If the context is insufficient, say you don't know. Include citations."
)

def answer_with_context(query: str, settings) -> Dict[str, Any]:
    hits = retrieve_top_k(query, settings, k=8)
    context = "\n\n".join(
        [f"{h['text']}\n[source: {h.get('source','unknown')}]" for h in hits]
    )
    text = generate(context=context, question=query, system=SYSTEM, model=settings.MODEL_NAME)
    return {
        "query": query,
        "answer": text,
        "citations": [h.get("source") for h in hits],
        "retrieval": {"k": len(hits)}
    }
