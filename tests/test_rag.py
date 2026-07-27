import os
import shutil
import pytest
from src.backend import rag_pipeline

# --- Paths to sample files ---
DATA_DIR = "data"
SAMPLE_TXT = os.path.join(DATA_DIR, "sample.txt")
SAMPLE_PDF = os.path.join(DATA_DIR, "sample.pdf")
SAMPLE_MD = os.path.join(DATA_DIR, "sample.md")

# --- ChromaDB persistence directory ---
CHROMA_DIR = "chroma_store"

@pytest.fixture(autouse=True)
def clean_chroma_store():
    """
    Cleanup ChromaDB store before each test run.
    Ensures tests always start with a fresh vector database.
    """
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)
    os.makedirs(CHROMA_DIR, exist_ok=True)
    yield
    # Optional cleanup after test run
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

def test_add_and_query_txt():
    """End-to-end test: ingest TXT and query it."""
    class DummyFile:
        type = "text/plain"
        def read(self):
            return b"Hello world. This is a test document."

    dummy_file = DummyFile()
    assert rag_pipeline.add_document(dummy_file) is True

    response = rag_pipeline.get_answer("What does the document say?", top_k=1)
    assert "answer" in response
    assert isinstance(response["answer"], str)

def test_add_and_query_pdf():
    """End-to-end test: ingest PDF and query it."""
    if os.path.exists(SAMPLE_PDF):
        dummy_pdf = open(SAMPLE_PDF, "rb")
        dummy_pdf.type = "application/pdf"
        assert rag_pipeline.add_document(dummy_pdf) is True
        dummy_pdf.close()

        response = rag_pipeline.get_answer("Summarize the PDF.", top_k=1)
        assert "answer" in response
        assert isinstance(response["answer"], str)
    else:
        pytest.skip("sample.pdf not found in data/")

def test_add_and_query_md():
    """End-to-end test: ingest Markdown and query it."""
    if os.path.exists(SAMPLE_MD):
        dummy_md = open(SAMPLE_MD, "rb")
        dummy_md.type = "text/markdown"
        assert rag_pipeline.add_document(dummy_md) is True
        dummy_md.close()

        response = rag_pipeline.get_answer("Summarize the markdown file.", top_k=1)
        assert "answer" in response
        assert isinstance(response["answer"], str)
    else:
        pytest.skip("sample.md not found in data/")

def test_get_answer_basic():
    """
    Test querying the knowledge base without ingestion.
    Ensures get_answer() runs even if no docs are present.
    """
    query = "What is this document about?"
    response = rag_pipeline.get_answer(query, top_k=1, temperature=0.0)

    assert "answer" in response
    assert isinstance(response["answer"], str)
    assert "retrieved_chunks" in response
    assert isinstance(response["retrieved_chunks"], list)
