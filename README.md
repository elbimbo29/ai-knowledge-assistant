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