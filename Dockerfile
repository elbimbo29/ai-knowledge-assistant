# ---------- Builder stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies needed for rpds-py, ChromaDB, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Ensure venv is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy project files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_PORT=8501

# Healthcheck: verify Streamlit responds on port 8501
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
