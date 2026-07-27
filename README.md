# AI Knowledge Assistant
> A Streamlit + RAG-based AI assistant powered by OpenAI, ChromaDB, and LangChain.  
> It allows you to upload documents (PDF, TXT, MD), embed them into a vector database, and query them using GPT for contextual answers.

![CI/CD Pipeline](https://github.com/<YOUR_USERNAME>/ai-knowledge-assistant/actions/workflows/deploy.yml/badge.svg)
<!-- Badge shows CI/CD status (✅ passing / ❌ failing / ⏳ running) -->

---

## 🚀 Features
- Document ingestion: PDF, TXT, Markdown
- Chunking + embeddings with OpenAI
- Persistent vector store using ChromaDB
- Retrieval + generation pipeline with GPT
- Streamlit UI for easy interaction
- Full test coverage with pytest
- CI/CD pipeline with GitHub Actions
- Automatic deployment to Render via Docker

---

## 🧩 Local Development
```bash
# Clone repo
git clone https://github.com/<YOUR_USERNAME>/ai-knowledge-assistant.git
cd ai-knowledge-assistant

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
