# 🤖 AI Knowledge Assistant
An end‑to‑end **Retrieval‑Augmented Generation (RAG)** application built with **Streamlit**, **LangChain**, **ChromaDB**, and **OpenAI**.  
It allows users to upload documents, query them via natural language, and receive context‑aware answers.

## 🗂 Project Structure
ai-knowledge-assistant/
├── app.py                 # Streamlit UI
├── requirements.txt       # Dependencies
├── Dockerfile             # Containerization
├── .dockerignore          # Docker exclusions
├── .github/workflows/     # CI/CD pipeline
│   └── deploy.yml
├── src/backend/           # Backend logic
│   ├── rag_pipeline.py    # Core RAG pipeline
│   ├── retrieve.py        # UI → Pipeline bridge
│   ├── chroma_index.py    # Direct ChromaDB access
│   └── init.py
├── tests/                 # Unit/integration tests
├── chroma_db/             # Persistent vector storage
└── README.md              # Documentation

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

## ⚙️ Local Development Setup

Follow these steps to get the AI Knowledge Assistant running on your local machine:

### 1. [Clone the repository](ca://s?q=Clone_repository)
```bash
git clone https://github.com/your-username/ai-knowledge-assistant.git
cd ai-knowledge-assistant

2. Install dependencies
pip install -r requirements.txt

3. Set environment variables
Create a .env file in the project root and add your OpenAI key:
OPENAI_API_KEY=your_openai_key

4. Run locally
streamlit run app.py

5. Run tests
pytest --maxfail=1 --disable-warnings -q

---

## ☁️ Cloud Deployment Setup

Follow these steps to deploy the AI Knowledge Assistant using Docker, GitHub Actions, GHCR, and Render:

### 1. [Build Docker image](ca://s?q=Build_Docker_image)
```bash
docker build -t ai-assistant .

2. Run Docker locally
docker run -p 8501:8501 ai-assistant

3. Push image to GHCR
Authenticate with GitHub Container Registry:
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
docker tag ai-assistant ghcr.io/USERNAME/ai-assistant:latest
docker push ghcr.io/USERNAME/ai-assistant:latest

4. CI/CD pipeline
Build & Test → runs pytest in mock/real modes.

Docker Build & Push → pushes image to GHCR.

Deploy to Render → triggers Render API deployment automatically.

5. Deploy to Render
Connect your GitHub repo to Render.
Configure environment variables (OPENAI_API_KEY).
Render pulls the Docker image from GHCR and hosts the app.
Access your app via Render’s public URL.


🚀 Deployment
CI/CD Pipeline
Build & Test → runs pytest in mock/real modes.

Docker Build & Push → pushes image to GHCR.

Deploy to Render → triggers Render API deployment.

## ⚙️ Manual Deployment
docker build -t ai-assistant .
docker run -p 8501:8501 ai-assistant


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


👨‍💻 Author
Built by Bimbo — transitioning into AI engineering, focusing on RAG systems, deployment workflows, and applied LLMs.




