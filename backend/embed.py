import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import PyPDF2
import markdown

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(path="data/"):
    """
    Load documents from the data/ folder.
    Supports .txt, .md, and .pdf files.
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
            pdf_reader = PyPDF2.PdfReader(filepath)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
            docs.append(pdf_text)

    return docs

def chunk_text(text, chunk_size=500):
    """
    Split a document into smaller chunks.
    Default chunk size = 500 words.
    """
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words, chunk_size))]

def build_index(chunks):
    """
    Convert text chunks into embeddings and store them in a FAISS index.
    """
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

def save_index(index, path="embeddings/faiss.index"):
    """
    Save FAISS index to disk.
    """
    faiss.write_index(index, path)

def load_index(path="embeddings/faiss.index"):
    """
    Load FAISS index from disk if it exists.
    Returns the FAISS index object or None if not found.
    """
    if os.path.exists(path):
        print("Loading FAISS index from disk...")
        return faiss.read_index(path)
    else:
        print("No FAISS index found. Please build a new one.")
        return None

if __name__ == "__main__":
    # Step 1: Try loading existing index
    index = load_index()

    if index is None:
        print("No existing index found. Building new one...")
        docs = load_documents()
        chunks = []
        for doc in docs:
            chunks.extend(chunk_text(doc))
        index, embeddings = build_index(chunks)
        save_index(index)
        print(f"Stored {len(chunks)} chunks in FAISS index.")
    else:
        print("FAISS index loaded successfully.")
