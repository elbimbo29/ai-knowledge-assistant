import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


# Use the key automatically
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini")


# --- Initialize Embeddings & LLM ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# --- Persistent ChromaDB store ---
CHROMA_DIR = "chroma_store"
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

# --- Add Document to Knowledge Base ---
def add_document(uploaded_file):
    """Ingest uploaded PDF or TXT into ChromaDB."""
    if uploaded_file.type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages])
    else:
        text = uploaded_file.read().decode("utf-8")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)

    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore.add_documents(docs)
    vectorstore.persist()

# --- Query Knowledge Base ---
def get_answer(query, top_k=3, temperature=0.3):
    """Retrieve context from ChromaDB and generate answer with GPT."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    retrieved_docs = retriever.get_relevant_documents(query)

    # Format context for display
    retrieved_chunks = [
        {"chunk": doc.page_content, "score": doc.metadata.get("score", 0.0)}
        for doc in retrieved_docs
    ]

    # Build prompt
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}"

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "retrieved_chunks": retrieved_chunks
    }
