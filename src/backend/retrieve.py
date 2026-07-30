# ============================================================
# retrieve.py (deprecated)
# Purpose: Thin wrapper around rag_pipeline for backwards compatibility.
# ============================================================

from src.backend.rag_pipeline import rag_pipeline

def get_answer(query, top_k=3, temperature=0.3):
    """
    Pass-through to rag_pipeline.get_answer().
    Supports temperature for consistency with app.py.
    """
    return rag_pipeline.get_answer(query, top_k=top_k, temperature=temperature)

def add_document(uploaded_file):
    """
    Pass-through to rag_pipeline.add_document().
    """
    return rag_pipeline.add_document(uploaded_file)

def save():
    """
    Optional: force persistence of ChromaDB to disk.
    """
    return rag_pipeline.save()
