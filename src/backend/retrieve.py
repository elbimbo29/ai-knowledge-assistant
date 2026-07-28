from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Initialize embedding model (same as in embed.py)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Connect to Chroma persistent store
# persist_directory ensures vectors are saved to disk and reloaded later
vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)

def search_index(query, top_k=3):
    """
    Retrieve context for a query:
    - Convert query into embedding
    - Search Chroma vector store for top_k nearest chunks
    - Return structured results with text + score
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
    Wrapper function expected by app.py.
    Uses search_index to retrieve relevant chunks and combines them.
    Returns both a combined answer string and the structured results.
    """
    results = search_index(query, top_k=top_k)
    answer = "\n".join([r["chunk"] for r in results])  # merge chunks into one string
    return answer, results

def add_document(text):
    """
    Add a new document chunk into Chroma.
    Useful for dynamically updating the knowledge base.
    """
    vectorstore.add_texts([text])
    vectorstore.persist()   # save changes to disk

if __name__ == "__main__":
    # Example usage for testing
    query = "What are the key concepts of AI?"
    answer, results = get_answer(query, top_k=3)

    print("Retrieved Context:")
    for r in results:
        print(f"- Score: {r['score']:.4f} | Text: {r['chunk'][:150]}...")
