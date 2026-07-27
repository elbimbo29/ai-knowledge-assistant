import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the same embedding model used in embed.py
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_index(query, index, chunks, top_k=3):
    """
    Retrieve context for a query:
    - Convert query into embedding
    - Search FAISS index for top_k nearest chunks
    - Return structured results with text + score
    """
    # Step 1: Convert query to embedding
    query_embedding = model.encode([query])

    # Step 2: Perform similarity search
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Step 3: Collect results
    results = []
    for rank, i in enumerate(indices[0]):
        results.append({
            "chunk": chunks[i],
            "score": float(distances[0][rank])  # lower score = closer match
        })

    return results

if __name__ == "__main__":
    from embed import load_index, load_documents, chunk_text, build_index

    # Load or rebuild index
    index = load_index()
    docs = load_documents()
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    if index is None:
        index, embeddings = build_index(chunks)

    # Test query
    query = "What are the key concepts of AI?"
    results = search_index(query, index, chunks, top_k=3)

    print("Retrieved Context:")
    for r in results:
        print(f"- Score: {r['score']:.4f} | Text: {r['chunk'][:150]}...")
