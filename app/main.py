import streamlit as st
from backend.rag_pipeline import get_answer

# Streamlit UI setup
st.set_page_config(page_title="AI Knowledge Assistant", layout="centered")

st.title("🤖 AI Knowledge Assistant")
st.write("Ask me anything, and I'll answer using your knowledge base.")

# User input
query = st.text_input("Enter your question:")

# Generate answer when query is submitted
if query:
    with st.spinner("Searching knowledge base..."):
        response = get_answer(query)

    # Display final answer
    st.success("Answer:")
    st.write(response["answer"])

    # Display retrieved context
    st.info("Retrieved Context:")
    for r in response["retrieved_chunks"]:
        st.write(f"- Score: {r['score']:.4f} | Text: {r['chunk'][:200]}...")
