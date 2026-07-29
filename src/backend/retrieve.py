from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# --- Embedding Model Initialization ---
# Purpose: Convert text into numerical vector representations.
# Model: "text-embedding-3-small" (efficient, lower cost).
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# --- Vector Store Setup ---
# Purpose: Connect to Chroma persistent store for saving/retrieving embeddings.
# persist_directory ensures vectors are saved to disk and reloaded later.
vectorstore = Chroma(
    collection_name="documents",          # logical grouping of documents
    embedding_function=embeddings,        # embedding model used for indexing
    persist_directory="chroma_db"         # folder where vectors are stored
)

def search_index(query, top_k=3):
    """
    Purpose:
      - Retrieve context for a query from ChromaDB.
      - Steps:
        1. Convert query into embedding.
        2. Search vector store for top_k nearest chunks.
        3. Return structured results with text + similarity score.
    Returns:
      - List of dicts with 'chunk' (text) and 'score' (similarity).
    """
    results = vectorstore.similarity_search_with_score(query, k=top_k)

    structured = []
    for doc, score in results:
        structured.append({
            "chunk": doc.page_content,   # actual text content
            "score": float(score)        # similarity score (lower = closer match)
        })

    return structured

def get_answer(query, top_k=3):
    """
    Purpose:
      - Wrapper function expected by app.py.
      - Uses search_index() to retrieve relevant chunks.
      - Combines chunks into a single answer string.
    Returns:
      - Tuple: (answer string, structured results list).
    """
    results = search_index(query, top_k=top_k)
    answer = "\n".join([r["chunk"] for r in results])  # merge chunks into one string
    return answer, results

def add_document(text):
    """
    Purpose:
      - Add a new document chunk into ChromaDB.
      - Useful for dynamically updating the knowledge base.
    Steps:
      - Embed text and add to vectorstore.
      - Persist changes to disk for future queries.
    """
    vectorstore.add_texts([text])
    vectorstore.persist()   # save changes to disk

if __name__ == "__main__":
    # --- Example Usage for Testing ---
    # Purpose: Run a sample query when executing this file directly.
    query = "What are the key concepts of AI?"
    answer, results = get_answer(query, top_k=3)

    print("Retrieved Context:")
    for r in results:
        print(f"- Score: {r['score']:.4f} | Text: {r['chunk'][:150]}...")
