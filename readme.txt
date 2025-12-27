Architecture:
frontend (React or simple HTML)
        |
        v
[ Flask API ]
  ├── /ingest        # ETL: pull open data, clean, chunk, store
  ├── /index         # compute embeddings, upsert into vector DB
  ├── /search        # retrieve (hybrid lexical + vector)
  ├── /rag           # retrieve + generate grounded answer (LLM)
  └── /health
        |
        v
[Storage]
  ├── data/raw/clean        # CSV/JSON/GeoJSON, cache API responses
  ├── Postgres/SQLite       # metadata & relational facts
  └── Qdrant (vector DB)    # embeddings + payloads

[Retrieval]
  ├── BM25 (whoosh/elastic-lite)  # optional lexical index
  ├── Qdrant vector search        # cosine similarity
  └── Reranker (optional)         # cross-encoder for relevance

[LLM & Embeddings]
  ├── sentence-transformers       # e.g., all-MiniLM-L6-v2 (free)
  └── Ollama local LLM            # e.g., mistral / llama3

[DAG/Automation]
  └── simple cron or Prefect (free) for scheduled ingestion






How to Run:


$env:OPENAQ_API_KEY = "test"
python -m app.pipelines.ingest_openaq

python -m app.pipelines.ingest_openaq
python -m app.pipelines.ingest_osm
python -m app.pipelines.ingest_gtfs


installation and build

python scripts/build_index.py


check build 

# List the output files
Get-Item .\data\index\faiss.index, .\data\index\meta.jsonl | Format-Table Name,Length,LastWriteTime

# Count how many metadata rows were written (lines = vectors)
(Get-Content .\data\index\meta.jsonl).Count



run

$env:OPENAQ_API_KEY = "aaf4de9cc76e9fb71694308b5a4da761f1929d543a23b0432f869b782e8df688"
python -m app.pipelines.ingest_openaq


results = store.search(query_embedding, top_k=8)


run

1: run flask 

python -c "from app.app import app; app.run(host='0.0.0.0', port=8000)"


2. ask query : 
curl -X POST http://localhost:8000/search/ `  -H "Content-Type: application/json" `-d '{"query":"Where are bike lanes near downtown?"}'


3.python request: 
import requests
r = requests.post("http://localhost:8000/rag/", json={"query":"Where are bike lanes near downtown and what is PM2.5 there now?"})
print(r.status_code, r.json())



Second run way: 
 .\scripts\run_server.ps1   


How it works in your code:


Retrieve:

Your question → converted to an embedding (vector).
FAISS searches your indexed chunks (from OpenAQ, OSM, GTFS).
Top relevant chunks are returned.



Augment:

These chunks are combined into a context string.
The context + your question → sent to the LLM.



Generate:

The LLM (via Ollama) produces an answer based only on that context.
It includes citations from the chunks.







# RAG-Search 🔍🧠

An advanced Retrieval-Augmented Generation (RAG) system designed to enhance large language model responses by grounding them in relevant, external knowledge sources.

## 🎯 Problem Statement
Large Language Models can generate fluent answers but may:
- Hallucinate facts
- Lack access to up-to-date or domain-specific knowledge
- Fail on knowledge-intensive queries

This project addresses these limitations by integrating a retrieval layer that injects relevant context into the generation pipeline.

## 🧠 System Architecture
The system follows a modular RAG pipeline:

Query  
→ Embedding Generation  
→ Vector Similarity Search  
→ Context Selection  
→ LLM Prompt Augmentation  
→ Answer Generation  

This design separates retrieval from generation, enabling scalability and component-level optimization.

## 🔍 Retrieval Strategy
- Dense vector embeddings for semantic search
- Similarity-based ranking (top-k retrieval)
- Context window optimization to reduce prompt noise

The retrieval layer is intentionally decoupled to allow:
- Swapping vector databases
- Experimenting with embedding models
- Domain-specific tuning

## 🧪 Generation Strategy
- Prompt construction includes:
  - Retrieved context
  - Query intent
  - Guardrails against hallucination
- Generation focuses on **grounded responses**, not creative completion

## 🛠 Tech Stack
- Python
- LLM APIs
- Embedding models
- Vector search (FAISS / equivalent)
- Modular prompt engineering

## ⚙️ Design Decisions
- **Why RAG instead of fine-tuning?**  
  Faster iteration, lower cost, easier knowledge updates.
- **Why modular components?**  
  Enables independent optimization and testing.
- **Why similarity search?**  
  Robust semantic retrieval over keyword matching.

## 📈 Use Cases
- Enterprise knowledge assistants
- Technical documentation Q&A
- Research paper retrieval
- Internal search systems

## ⚠️ Limitations
- Retrieval quality depends on embedding choice
- Context length constrained by LLM limits
- Performance varies by domain density

## 🚀 Future Work
- Hybrid retrieval (keyword + dense)
- Reranking with cross-encoders
- Query rewriting and intent detection
- Evaluation metrics for retrieval quality

## 👩‍💻 Author
Fatemeh Mosleh  
MSc Artificial Intelligence (Distinction)



