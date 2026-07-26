import streamlit as st
from backend.rag_pipeline import get_answer

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
            Powered by RAG • Built with Python, FAISS, and GPT
        </p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Controls")
top_k = st.sidebar.slider("Number of context chunks (top_k)", 1, 10, 3)
temperature = st.sidebar.slider("Generation creativity (temperature)", 0.0, 1.0, 0.3)
st.sidebar.markdown("---")
st.sidebar.write("👤 Built by **Bimbo**")
st.sidebar.write("[GitHub Repository](https://github.com/your-username/ai-knowledge-assistant)")
st.sidebar.write("Technologies: Python • FAISS • GPT • Streamlit")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display Chat History ---
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if query := st.chat_input("💬 Ask me anything..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.spinner("🔎 Searching knowledge base..."):
        response = get_answer(query, top_k=top_k)

    answer = response["answer"]

    # --- Answer Display ---
    st.markdown(
        """
        <div style="background-color:#e8f5e9; padding:15px; border-radius:8px;">
            <h3 style="color:#2e7d32;">✅ Answer</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write(answer)

    # Add assistant message to history
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # --- Context Display ---
    with st.expander("📚 Retrieved Context"):
        for idx, r in enumerate(response["retrieved_chunks"], start=1):
            st.markdown(f"**Chunk {idx}** (Score: {r['score']:.4f})")
            st.write(r["chunk"])
            st.markdown("---")
