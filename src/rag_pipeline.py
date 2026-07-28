import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_MOCK = os.getenv("USE_MOCK", "False").lower() == "true"
USE_MEMORY_DB = os.getenv("USE_MEMORY_DB", "False").lower() == "true"

# --- LangChain imports ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter



from langchain_chroma import Chroma   # updated import
from langchain_core.documents import Document
from pypdf import PdfReader           # updated import


class RAGPipeline:
    """
    Class-based RAG pipeline.
    Provides add_document(), get_answer(), and run() methods.
    """

    def __init__(self):
        self.embeddings = None
        self.llm = None
        self.vectorstore = None

        if OPENAI_API_KEY:
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

            if USE_MEMORY_DB:
                # In-memory Chroma (no folder, no locked files)
                self.vectorstore = Chroma(embedding_function=self.embeddings)
            else:
                # Persistent Chroma (creates chroma_store folder)
                self.CHROMA_DIR = "chroma_store"
                self.vectorstore = Chroma(
                    persist_directory=self.CHROMA_DIR,
                    embedding_function=self.embeddings
                )

    def add_document(self, uploaded_file):
        """
        Ingest uploaded PDF, TXT, or MD file into ChromaDB.
        Splits into chunks, embeds, and persists them.
        """
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = uploaded_file.read().decode("utf-8")

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_text(text)

            docs = [Document(page_content=chunk) for chunk in chunks]
            self.vectorstore.add_documents(docs)
            if not USE_MEMORY_DB:
                # Chroma >=0.4 auto-persists, but keep for compatibility
                try:
                    self.vectorstore.persist()
                except Exception:
                    pass
            return True

        except Exception as e:
            raise RuntimeError(f"Failed to add document: {e}")

    def get_answer(self, query, top_k=3, temperature=0.3):
        """
        Retrieve context from ChromaDB and generate answer with GPT.
        Returns both the answer and retrieved chunks for display.
        """
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
            # FIX: use invoke() instead of get_relevant_documents()
            retrieved_docs = retriever.invoke(query)

            retrieved_chunks = [
                {"chunk": doc.page_content, "score": doc.metadata.get("score", 0.0)}
                for doc in retrieved_docs
            ]

            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}"

            response = self.llm.invoke(prompt)

            return {
                "answer": response.content,
                "retrieved_chunks": retrieved_chunks
            }

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve answer: {e}")

    def run(self, documents, query, mock: bool = False):
        """
        Unified RAG pipeline:
        - Accepts raw text documents (list of strings)
        - Splits, embeds, and stores them in ChromaDB
        - Runs a query against the knowledge base
        - If mock=True, USE_MOCK, or no API key → returns canned answer
        """
        if mock or USE_MOCK or not OPENAI_API_KEY:
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
        if not USE_MEMORY_DB:
            try:
                self.vectorstore.persist()
            except Exception:
                pass

        return self.get_answer(query)


# --- Expose a default instance for convenience ---
rag_pipeline = RAGPipeline()
