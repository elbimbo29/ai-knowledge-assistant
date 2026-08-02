# ============================================================
# rag_pipeline.py
# Purpose: Implements the Retrieval-Augmented Generation (RAG) pipeline.
# - Handles document ingestion (PDF, TXT/MD) and chunking
# - Embeds text using OpenAI embeddings
# - Stores/retrieves vectors in ChromaDB (persistent or in-memory)
# - Generates answers with GPT using retrieved context
# ============================================================
# ============================================================
# rag_pipeline.py
# Purpose: Implements the Retrieval-Augmented Generation (RAG) pipeline.
# ============================================================

import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_MEMORY_DB = os.getenv("USE_MEMORY_DB", "False").lower() == "true"

# --- LangChain imports ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pypdf import PdfReader


class RAGPipeline:
    def __init__(self):
        self.embeddings = None
        self.llm = None
        self.vectorstore = None

        # Initialize embeddings/LLM only if API key is present and not in mock mode
        if OPENAI_API_KEY and not self._use_mock():
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

            if USE_MEMORY_DB:
                self.vectorstore = Chroma(embedding_function=self.embeddings)
            else:
                self.CHROMA_DIR = "chroma_store"
                self.vectorstore = Chroma(
                    persist_directory=self.CHROMA_DIR,
                    embedding_function=self.embeddings
                )

    def _use_mock(self) -> bool:
        """Check mock mode dynamically from environment."""
        return os.getenv("USE_MOCK", "real").lower() == "mock"

    def add_document(self, uploaded_file):
        """Ingest uploaded PDF or TXT/MD file into ChromaDB."""
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = uploaded_file.read().decode("utf-8").strip()

            if not text:
                raise ValueError("⚠️ Uploaded file is empty or unreadable.")

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_text(text)
            docs = [Document(page_content=chunk) for chunk in chunks]

            if self.vectorstore:
                self.vectorstore.add_documents(docs)
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to add document: {e}")

    def get_answer(self, query, top_k=3, temperature=0.3):
        if self._use_mock() or not OPENAI_API_KEY:
            return {
                "answer": f"[MOCK ANSWER] Query='{query}'",
                "retrieved_chunks": []
            }

        results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        retrieved_chunks = [
            {"chunk": doc.page_content, "score": float(score)}
            for doc, score in results
        ]

        context = "\n\n".join([doc.page_content for doc, _ in results])
        prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}"

        response = self.llm.invoke(prompt)

        return {
            "answer": response.content,
            "retrieved_chunks": retrieved_chunks
        }

    def run(self, documents, query):
        if self._use_mock() or not OPENAI_API_KEY:
            return {
                "answer": f"[MOCK ANSWER] Query='{query}' | Docs={len(documents)}",
                "retrieved_chunks": [{"chunk": doc, "score": 1.0} for doc in documents]
            }

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = []
        for text in documents:
            chunks = splitter.split_text(text)
            docs.extend([Document(page_content=chunk) for chunk in chunks])

        self.vectorstore.add_documents(docs)
        return self.get_answer(query)

    def save(self):
        if not USE_MEMORY_DB and self.vectorstore:
            self.vectorstore._client.persist()


# --- Expose a default instance ---
rag_pipeline = RAGPipeline()
