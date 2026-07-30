# ============================================================
# app.py
# Purpose: Streamlit frontend for the AI Knowledge Assistant.
# - Provides user interface for queries and file uploads
# - Handles chat history and context display
# - Connects directly to rag_pipeline backend
# ============================================================

import sys, os
# --- Path Setup ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
from src.backend import rag_pipeline   # ✅ Import global instance

# --- Secure API Key Handling ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("⚠️ OPENAI_API_KEY not found. Please set it in your environment or GitHub Secrets.")
    st.stop()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)

# --- Branding Header ---
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color:#4CAF50;">🤖 AI Knowledge Assistant</h1>
        <p style="font-size:18px; color:gray;">
            Powered by RAG • Built with Python, ChromaDB, and GPT
        </p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Controls")
top_k = st.sidebar.slider("Number of context chunks (top_k)", 1, 10, st.session_state.get("top_k", 3))
temperature = st.sidebar.slider("Generation creativity (temperature)", 0.0, 1.0, st.session_state.get("temperature", 0.3))
st.session_state["top_k"] = top_k
st.session_state["temperature"] = temperature

st.sidebar.markdown("---")
st.sidebar.write("👤 Built by **Bimbo**")
st.sidebar.write("[GitHub Repository](https://github.com/elbimbo29/ai-knowledge-assistant)")
st.sidebar.write("Technologies: Python • ChromaDB • GPT • Streamlit")

# --- File Upload for RAG ---
uploaded_file = st.sidebar.file_uploader("📂 Upload a document", type=["pdf", "txt"])
if uploaded_file:
    with st.spinner("📥 Adding document to knowledge base..."):
        try:
            rag_pipeline.add_document(uploaded_file)   # ✅ Pipeline handles parsing internally
            st.sidebar.success("✅ Document added successfully!")
        except Exception as e:
            st.sidebar.error(f"⚠️ Failed to add document: {e}")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display Chat History ---
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if query := st.chat_input("💬 Ask me anything..."):
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        with st.spinner("🔎 Searching knowledge base..."):
            response = rag_pipeline.get_answer(query, top_k=top_k, temperature=temperature)

        answer = response.get("answer", "⚠️ No answer generated.")
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

        if "retrieved_chunks" in response:
            with st.expander("📚 Retrieved Context"):
                for idx, r in enumerate(response["retrieved_chunks"], start=1):
                    st.markdown(f"**Chunk {idx}** (Score: {r.get('score', 0):.4f})")
                    st.write(r.get("chunk", "⚠️ Missing chunk"))
                    st.markdown("---")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# --- Footer ---
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:14px;">
        © 2026 Bimbo • AI Knowledge Assistant
    </div>
    """,
    unsafe_allow_html=True
)
