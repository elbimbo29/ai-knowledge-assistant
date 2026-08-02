"""
tests/test_rag.py
Unit tests for rag_pipeline and helper functions.
"""

import os
import pytest
from src.rag_pipeline import rag_pipeline   # class instance with add_document, get_answer, run

# --- Force in-memory Chroma for tests ---
os.environ["USE_MEMORY_DB"] = "True"

DATA_DIR = "data"
SAMPLE_PDF = os.path.join(DATA_DIR, "sample.pdf")
SAMPLE_MD = os.path.join(DATA_DIR, "sample.md")


def test_rag_pipeline_mock():
    """
    Test rag_pipeline in mock mode.
    This avoids needing an OpenAI API key and ensures CI/CD can run safely.
    """
    docs = ["The Eiffel Tower is in Paris.", "The Colosseum is in Rome."]
    query = "Where is the Eiffel Tower?"

    result = rag_pipeline.run(docs, query, mock=True)

    assert "MOCK ANSWER" in result["answer"]
    assert len(result["retrieved_chunks"]) == 2
    assert query in result["answer"]


def test_add_and_query_txt():
    """
    End-to-end test: ingest TXT and query it.
    """
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
    """
    End-to-end test: ingest PDF and query it.
    Skips if sample.pdf is not found in data/.
    """
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
    """
    End-to-end test: ingest Markdown and query it.
    Skips if sample.md is not found in data/.
    """
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


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="Requires OPENAI_API_KEY for real mode"
)
def test_rag_pipeline_real_mode():
    """
    Real mode test: runs only if OPENAI_API_KEY is set.
    Validates actual retrieval + LLM integration.
    """
    # Skip if USE_MOCK is set to "mock"
    if os.getenv("USE_MOCK") == "mock":
        pytest.skip("Skipping real mode test because USE_MOCK=mock")

    docs = ["The Eiffel Tower is in Paris."]
    query = "Where is the Eiffel Tower?"

    result = rag_pipeline.run(docs, query)

    # Expect GPT to mention "Paris" in the answer
    assert "Paris" in result["answer"]
