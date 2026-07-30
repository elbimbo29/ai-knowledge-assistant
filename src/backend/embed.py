# ============================================================
# embed.py
# Purpose: Build and manage a Chroma index for document embeddings.
# - Loads documents from /data (txt, md, pdf)
# - Splits text into chunks
# - Embeds chunks using OpenAI embeddings
# - Stores/retrieves vectors in ChromaDB (persistent or in-memory)
# ============================================================

import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import pypdf          # modern PDF library (replacement for PyPDF2)
import markdown       # for parsing .md files into text

# Initialize embedding model (same as in retrieve.py)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def load_documents(path="data/"):
    """
    Load documents from the data/ folder.
    Supports .txt, .md, and .pdf files.
    Returns a list of raw text strings.
    """
    docs = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                docs.append(f.read())

        elif filename.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                md_content = f.read()
                html = markdown.markdown(md_content)
                plain_text = "".join(html.split("<")[0::2])  # strip tags
                docs.append(plain_text)

        elif filename.endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(filepath)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
            docs.append(pdf_text)

    return docs

def chunk_text(text, chunk_size=500):
    """
    Split a document into smaller chunks.
    Default chunk size = 500 words.
    Returns a list of text chunks.
    """
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_index(chunks, persist_directory="chroma_db"):
    """
    Convert text chunks into embeddings and store them in a Chroma collection.
    Persistence is automatic when persist_directory is set.
    """
    vectorstore = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.add_texts(chunks)
    return vectorstore

def save_index(vectorstore):
    """
    Force persistence of ChromaDB to disk.
    Useful if you want to explicitly flush changes.
    """
    try:
        vectorstore._client.persist()
    except Exception as e:
        raise RuntimeError(f"Failed to persist vectorstore: {e}")

def load_index(persist_directory="chroma_db"):
    """
    Load Chroma collection from disk if it exists.
    Returns the Chroma vectorstore object or None if not found.
    """
    if os.path.exists(persist_directory):
        print("Loading Chroma index from disk...")
        return Chroma(
            collection_name="documents",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
    else:
        print("No Chroma index found. Please build a new one.")
        return None

if __name__ == "__main__":
    # Step 1: Try loading existing index
    vectorstore = load_index()

    if vectorstore is None:
        print("No existing index found. Building new one...")
        docs = load_documents()
        chunks = []
        for doc in docs:
            chunks.extend(chunk_text(doc))
        vectorstore = build_index(chunks)
        save_index(vectorstore)   # ✅ Explicit flush
        print(f"Stored {len(chunks)} chunks in Chroma collection.")
    else:
        print("Chroma index loaded successfully.")
