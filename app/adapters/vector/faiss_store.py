
import faiss, os, json
import numpy as np

class FaissStore:
    def __init__(self, index_path: str, meta_path: str):
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = None
        self.meta = []
        self._load()

    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            # default L2 index for 384-d embeddings (MiniLM)
            self.index = faiss.IndexFlatL2(384)
        if os.path.exists(self.meta_path):
            self.meta = [json.loads(l) for l in open(self.meta_path)]
        else:
            self.meta = []

    def add(self, vectors: np.ndarray, payloads):
        assert vectors.shape[1] == 384, "expected 384-d embeddings"
        start = len(self.meta)
        self.index.add(vectors.astype("float32"))
        self.meta.extend(payloads)
        # persist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            for p in self.meta:
                f.write(json.dumps(p) + "\n")

    def search(self, query_vec, top_k=8):
        q = np.array(query_vec, dtype="float32").reshape(1, -1)
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.meta): continue
            results.append({"id": int(idx), "score": float(dist), "payload": self.meta[idx]})
        return results
