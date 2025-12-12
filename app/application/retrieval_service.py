
from typing import List, Dict
from ..adapters.vector.faiss_store import FaissStore
from ..adapters.embed.sentence import embed_text

def retrieve_top_k(query: str, settings, k: int = 8) -> List[Dict]:
    store = FaissStore(index_path=settings.FAISS_INDEX_PATH, meta_path=settings.META_PATH)
    vec = embed_text(query)
    results = store.search(vec, top_k=k)
    # results: [{ "id":..., "score":..., "payload":{...} }]
    return [r["payload"] for r in results]
