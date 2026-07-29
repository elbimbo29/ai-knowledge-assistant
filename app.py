import sys, os
# --- Path Setup ---
# Purpose: Add "src" folder to Python path so backend modules can be imported.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
from src.backend.retrieve import get_answer, add_document   # Import backend functions

# --- Secure API Key Handling ---
# Purpose: Ensure OPENAI_API_KEY is available before running the app.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("⚠️ OPENAI_API_KEY not found. Please set it in your environment or GitHub Secrets.")
    st.stop()   # Stop app execution if key is missing

# --- Page Configuration ---
# Purpose: Configure Streamlit page settings (title, icon, layout).
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)

# --- Branding Header ---
# Purpose: Display app title, subtitle, and branding info at the top of the page.
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
# Purpose: Provide user controls for RAG parameters and app info.
st.sidebar.title("⚙️ Controls")
top_k = st.sidebar.slider("Number of context chunks (top_k)", 1, 10, st.session_state.get("top_k", 3))
temperature = st.sidebar.slider("Generation creativity (temperature)", 0.0, 1.0, st.session_state.get("temperature", 0.3))
st.session_state["top_k"] = top_k
st.session_state["temperature"] = temperature

# Sidebar branding and links
st.sidebar.markdown("---")
st.sidebar.write("👤 Built by **Bimbo**")
st.sidebar.write("[GitHub Repository](https://github.com/elbimbo29/ai-knowledge-assistant)")
st.sidebar.write("Technologies: Python • ChromaDB • GPT • Streamlit")

# --- File Upload for RAG ---
# Purpose: Allow user to upload PDF/TXT documents to add to knowledge base.
uploaded_file = st.sidebar.file_uploader("📂 Upload a document", type=["pdf", "txt"])
if uploaded_file:
    with st.spinner("📥 Adding document to knowledge base..."):
        try:
            add_document(uploaded_file)   # Backend ingestion
            st.sidebar.success("Document added successfully!")
        except Exception as e:
            st.sidebar.error(f"⚠️ Failed to add document: {e}")

# --- Initialize Chat History ---
# Purpose: Maintain conversation history across user queries.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display Chat History ---
# Purpose: Render past messages in chat format.
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
# Purpose: Capture user query and generate assistant response.
if query := st.chat_input("💬 Ask me anything..."):
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        with st.spinner("🔎 Searching knowledge base..."):
            response = get_answer(query, top_k=top_k, temperature=temperature)   # Backend query

        answer = response.get("answer", "⚠️ No answer generated.")

        # Save assistant response
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

        # --- Context Display ---
        # Purpose: Show retrieved chunks for transparency/debugging.
        if "retrieved_chunks" in response:
            with st.expander("📚 Retrieved Context"):
                for idx, r in enumerate(response["retrieved_chunks"], start=1):
                    st.markdown(f"**Chunk {idx}** (Score: {r.get('score', 0):.4f})")
                    st.write(r.get("chunk", "⚠️ Missing chunk"))
                    st.markdown("---")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# --- Footer ---
# Purpose: Display footer branding and copyright.
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:14px;">
        © 2026 Bimbo • AI Knowledge Assistant
    </div>
    """,
    unsafe_allow_html=True
)
