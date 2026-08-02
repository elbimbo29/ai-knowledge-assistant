# 🤖 AI Knowledge Assistant
An end‑to‑end Retrieval‑Augmented Generation (RAG) application powered by Streamlit, LangChain, ChromaDB, and OpenAI. This project enables users to upload documents, query them in natural language, and receive context‑aware answers through a clean, intuitive interface.

It features a CI/CD pipeline with GitHub Actions for automated builds and testing, and is deployed seamlessly to Render using Docker images published to GitHub Container Registry (GHCR).

## 🗂 Project Structure
ai-knowledge-assistant/
│
├── README.md                # Project overview, deployment docs, screenshots
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker build instructions
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow for CI/CD
│
├── src/                     # Application source code
│   ├── app.py               # Streamlit entry point
│   ├── rag_pipeline.py      # RAG logic (LangChain + ChromaDB)
│   ├── utils.py             # Helper functions
│   └── config.py            # Configs (API keys, paths, etc.)
│
├── tests/                   # Unit and integration tests
│   ├── test_app.py
│   └── test_rag_pipeline.py
│
└── images/                  # Screenshots (UI, deployment)
    ├── home-screen.png
    ├── file-upload.png
    ├── chat-interface.png
    └── results-display.png


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

📖 Documentation Phases

Phase 01 → Streamlit UI setup (app.py)
Phase 02 → Backend wrappers (retrieve.py)
Phase 03 → RAG pipeline (rag_pipeline.py)
Phase 04 → Chroma index (chroma_index.py)
Phase 05 → CI/CD workflow (deploy.yml)
Phase 06 → Requirements documentation
Phase 07 → Project structure
Phase 08 → Architecture diagram
Phase 09 → Sequence diagram
Phase 10 → Deployment diagram
Phase 11 → Component & layered architecture

🧪 Testing
Run tests with:  pytest --maxfail=1 --disable-warnings -q

---

## Application Screenshots

### Home Screen
![Home Screen](images/home-screen.png)
### File Upload
![File Upload](images/file-upload.png)
### Chat Interface
![Chat Interface](images/chat-interface.png)
### Docker Publish
![Results Display](images/docker-published.jpeg)
### Render Deployed
![Results Display](images/render-deployed.png)


