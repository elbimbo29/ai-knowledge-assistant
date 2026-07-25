from embed import load_index, load_documents, chunk_text, build_index
from retrieve import search_index
from generate import generate_answer

def get_answer(query, top_k=3):
    """
    End-to-end RAG pipeline:
    - Load or build FAISS index
    - Retrieve top_k relevant chunks
    - Generate grounded answer using GPT
    - Return final response
    """
    # Step 1: Load or rebuild index
    index = load_index()
    docs = load_documents()
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    if index is None:
        index, embeddings = build_index(chunks)

    # Step 2: Retrieve relevant chunks
    retrieved = search_index(query, index, chunks, top_k=top_k)
    retrieved_chunks = [r["chunk"] for r in retrieved]

    # Step 3: Generate answer
    answer = generate_answer(query, retrieved_chunks)

    # Step 4: Return RAG response
    return {
        "query": query,
        "retrieved_chunks": retrieved,
        "answer": answer
    }

if __name__ == "__main__":
    # Example usage
    query = "Explain the key concepts of artificial intelligence."
    response = get_answer(query)
    print("Final RAG Response:")
    print("Query:", response["query"])
    print("Answer:", response["answer"])
    print("Retrieved Context:")
    for r in response["retrieved_chunks"]:
        print(f"- Score: {r['score']:.4f} | Text: {r['chunk'][:150]}...")
