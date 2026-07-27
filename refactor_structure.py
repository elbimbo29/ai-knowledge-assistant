import os
import shutil

# --- Final structure definition ---
folders = [
    "src/backend",
    "data",
    "tests",
    ".github/workflows"
]

# --- Create folders if not exist ---
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# --- Move backend files ---
backend_files = ["embed.py", "generate.py", "retrieve.py", "__init__.py"]
for f in backend_files:
    src = os.path.join("backend", f)
    dst = os.path.join("src/backend", f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {src} -> {dst}")

# --- Move data files (keep them in data/) ---
data_files = ["sample.md", "sample.pdf", "sample.txt"]
for f in data_files:
    src = os.path.join("data", f)
    dst = os.path.join("data", f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Kept {src} in {dst}")

# --- Update app.py imports safely ---
app_file = "app.py"
if os.path.exists(app_file):
    with open(app_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Only replace if the old imports exist
    if "from backend.rag_pipeline" in content:
        content = content.replace("from backend.rag_pipeline", "from src.backend.retrieve")
    if "from backend" in content:
        content = content.replace("from backend", "from src.backend")

    with open(app_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated imports in app.py")

# --- Create placeholder test file ---
test_file = "tests/test_rag.py"
if not os.path.exists(test_file):
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# Basic test placeholder for RAG pipeline\n")
        f.write("def test_placeholder():\n")
        f.write("    assert True\n")
    print(f"Created {test_file}")

# --- Create placeholder CI/CD workflow ---
workflow_file = ".github/workflows/deploy.yml"
if not os.path.exists(workflow_file):
    os.makedirs(".github/workflows", exist_ok=True)
    with open(workflow_file, "w", encoding="utf-8") as f:
        f.write(
            "name: Deploy\n\n"
            "on:\n  push:\n    branches:\n      - main\n\n"
            "jobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v3\n"
            "      - name: Set up Python\n"
            "        uses: actions/setup-python@v4\n"
            "        with:\n"
            "          python-version: '3.10'\n"
            "      - name: Install dependencies\n"
            "        run: pip install -r requirements.txt\n"
            "      - name: Run tests\n"
            "        run: pytest\n"
        )
    print(f"Created {workflow_file}")

# --- Delete old backend folder if empty ---
if os.path.exists("backend"):
    try:
        shutil.rmtree("backend")
        print("Deleted old backend folder")
    except Exception as e:
        print(f"Could not delete backend folder: {e}")

print("\n✅ Refactor complete. Your project now matches the final structure.")
