# AI Knowledge Assistant
> A Streamlit + RAG-based AI assistant powered by OpenAI, ChromaDB, and LangChain.  
> It ingests documents (PDF, TXT, Markdown), indexes them in a vector database, and answers queries using OpenAI models.


# AI Knowledge Assistant

[![CI/CD Pipeline](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/deploy.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/deploy.yml)
[![Render Deploy](https://render.com/badges/<YOUR_RENDER_SERVICE_ID>)](https://<YOUR_RENDER_APP_URL>)
[![Docker Image](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/actions/workflows/deploy.yml/badge.svg?event=push)](https://ghcr.io/<YOUR_USERNAME>/<YOUR_REPO>/ai-knowledge-assistant:latest)
[![Version](https://img.shields.io/github/v/release/<YOUR_USERNAME>/<YOUR_REPO>?sort=semver)](https://github.com/<YOUR_USERNAME>/<YOUR_REPO>/releases)


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

## 🛠️ Troubleshooting

### GitHub Actions
- **Tests failing (❌ badge)**  
  - Run `pytest` locally to confirm errors.  
  - Check `tests/test_rag.py` → ensure sample files (`sample.pdf`, `sample.md`) exist in `data/`.  
  - If missing, tests will skip gracefully, but ingestion tests won’t run.

- **Docker build errors**  
  - Confirm `Dockerfile` is in repo root.  
  - Ensure `requirements.txt` includes all dependencies (Streamlit, LangChain, ChromaDB, PyPDF2, etc.).  
  - Run locally:  
    ```bash
    docker build -t ai-knowledge-assistant .
    ```

- **GHCR push fails**  
  - Check GitHub Actions logs for authentication issues.  
  - Ensure `GITHUB_TOKEN` is available (default in Actions).  
  - Verify image tag format:  
    ```
    ghcr.io/<YOUR_USERNAME>/ai-knowledge-assistant:latest
    ```

### Render Deployment
- **Deploy not triggered**  
  - Confirm GitHub secrets are set:  
    - `RENDER_API_KEY` → from Render account.  
    - `RENDER_SERVICE_ID` → from Render dashboard.  
  - Check `deploy-render` job logs in Actions.

- **App fails to start**  
  - Check Render logs → likely missing environment variables.  
  - Ensure `OPENAI_API_KEY` is set in Render dashboard.  
  - Confirm `STREAMLIT_PORT=8501`.

- **Health check failing**  
  - Verify `healthCheckPath: /` in `render.yaml`.  
  - Streamlit must serve on port `8501`.  
  - If using custom routes, adjust health check path.

- **App loads but queries fail**  
  - Double-check `OPENAI_API_KEY` validity.  
  - Ensure ChromaDB persistence directory (`chroma_store`) is writable in container.  
  - Run locally with same Docker image to reproduce.

---

## ✅ Quick Fix Checklist
- [ ] Run `pytest` locally before pushing.  
- [ ] Confirm Docker builds locally.  
- [ ] Verify GitHub secrets (`RENDER_API_KEY`, `RENDER_SERVICE_ID`).  
- [ ] Add environment variables in Render dashboard.  
- [ ] Check Render logs if deploy 

---

## 🧪 Testing Notes

### Import Path Issues
- Tests in `tests/test_rag.py` import modules from `src/` (e.g., `from src.backend import rag_pipeline`).
- By default, GitHub Actions and some local environments don’t include `src/` in the Python path.
- This caused the error:  ModuleNotFoundError: No module named 'src'

### Fixes Applied
- Added empty `__init__.py` files in both `src/` and `tests/` directories to make them proper Python packages.
- Updated CI workflow (`deploy.yml`) to run pytest with:
```bash
PYTHONPATH=$PYTHONPATH:$(pwd)/src pytest --maxfail=1 --disable-warnings -q
- This ensures Python can locate the src package during test runs.


