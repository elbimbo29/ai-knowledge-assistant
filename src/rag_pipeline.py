import os
from dotenv import load_dotenv

# --- Load environment variables ---
# Purpose: Load secrets and runtime flags from a .env file or environment.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")                  # OpenAI API key for embeddings/LLM
USE_MOCK = os.getenv("USE_MOCK", "False").lower() == "true"   # Flag to run in mock mode (no API calls)
USE_MEMORY_DB = os.getenv("USE_MEMORY_DB", "False").lower() == "true"  # Flag to use in-memory ChromaDB

# --- LangChain imports ---
# Purpose: Bring in LangChain components for embeddings, LLM, text splitting, and vector storage.
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma   # Vector database (ChromaDB)
from langchain_core.documents import Document
from pypdf import PdfReader           # PDF parsing library

class RAGPipeline:
    """
    Class-based RAG pipeline.
    Purpose: Provides methods to ingest documents, query them, and run a retrieval-augmented generation workflow.
    Methods:
      - add_document(): ingest and embed documents into ChromaDB
      - get_answer(): retrieve context and generate answers with GPT
      - run(): unified pipeline for ingestion + query
    """

    def __init__(self):
        # Initialize embeddings, LLM, and vectorstore depending on environment variables
        self.embeddings = None
        self.llm = None
        self.vectorstore = None

        if OPENAI_API_KEY:
            # Embeddings model for vectorization
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            # Chat model for answer generation
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

            if USE_MEMORY_DB:
                # In-memory Chroma (temporary, no persistence)
                self.vectorstore = Chroma(embedding_function=self.embeddings)
            else:
                # Persistent Chroma (stored in chroma_store folder)
                self.CHROMA_DIR = "chroma_store"
                self.vectorstore = Chroma(
                    persist_directory=self.CHROMA_DIR,
                    embedding_function=self.embeddings
                )

    def add_document(self, uploaded_file):
        """
        Purpose: Ingest uploaded PDF, TXT, or MD file into ChromaDB.
        Steps:
          - Extract text (PDF via PyPDF, others via UTF-8 decode)
          - Split into chunks
          - Embed and store in ChromaDB
          - Persist if using persistent DB
        Returns True if successful, raises RuntimeError otherwise.
        """
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = uploaded_file.read().decode("utf-8")

            # Split text into overlapping chunks for better retrieval
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_text(text)

            # Convert chunks into LangChain Document objects
            docs = [Document(page_content=chunk) for chunk in chunks]
            self.vectorstore.add_documents(docs)

            # Persist if using persistent DB (Chroma >=0.4 auto-persists, but kept for compatibility)
            if not USE_MEMORY_DB:
                try:
                    self.vectorstore.persist()
                except Exception:
                    pass
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to add document: {e}")

    def get_answer(self, query, top_k=3, temperature=0.3):
        """
        Purpose: Retrieve context from ChromaDB and generate an answer with GPT.
        Steps:
          - Use retriever to fetch top_k relevant chunks
          - Build a context-aware prompt
          - Invoke LLM to generate answer
        Returns: dict with 'answer' and 'retrieved_chunks'
        """
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
            retrieved_docs = retriever.invoke(query)   # Get relevant documents

            # Collect retrieved chunks for display/debugging
            retrieved_chunks = [
                {"chunk": doc.page_content, "score": doc.metadata.get("score", 0.0)}
                for doc in retrieved_docs
            ]

            # Build context prompt
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}"

            # Generate answer with LLM
            response = self.llm.invoke(prompt)

            return {
                "answer": response.content,
                "retrieved_chunks": retrieved_chunks
            }

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve answer: {e}")

    def run(self, documents, query, mock: bool = False):
        """
        Purpose: Unified RAG pipeline for raw text documents.
        Steps:
          - If mock=True, USE_MOCK, or no API key → return canned answer
          - Otherwise:
            - Split documents into chunks
            - Embed and store in ChromaDB
            - Persist if using persistent DB
            - Run query against knowledge base
        Returns: dict with 'answer' and 'retrieved_chunks'
        """
        if mock or USE_MOCK or not OPENAI_API_KEY:
            return {
                "answer": f"[MOCK ANSWER] Query='{query}' | Docs={len(documents)}",
                "retrieved_chunks": [{"chunk": doc, "score": 1.0} for doc in documents]
            }

        # Split and embed documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = []
        for text in documents:
            chunks = splitter.split_text(text)
            docs.extend([Document(page_content=chunk) for chunk in chunks])

        self.vectorstore.add_documents(docs)

        # Persist if using persistent DB
        if not USE_MEMORY_DB:
            try:
                self.vectorstore.persist()
            except Exception:
                pass

        return self.get_answer(query)


# --- Expose a default instance for convenience ---
# Purpose: Provide a ready-to-use pipeline instance without needing to instantiate manually.
rag_pipeline = RAGPipeline()
