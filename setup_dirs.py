import os

# Directories to ensure exist
dirs = ["backend", "chroma_store"]

for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory: {d}")
    else:
        print(f"Directory already exists: {d}")

# Ensure backend/__init__.py exists
init_file = os.path.join("backend", "__init__.py")
if not os.path.exists(init_file):
    with open(init_file, "w") as f:
        f.write("")  # empty file
    print("Created backend/__init__.py")
else:
    print("backend/__init__.py already exists")

# Ensure backend/rag_pipeline.py exists
rag_file = os.path.join("backend", "rag_pipeline.py")
if not os.path.exists(rag_file):
    with open(rag_file, "w") as f:
        f.write(
            "# Starter rag_pipeline.py\n"
            "def get_answer(query, top_k=3, temperature=0.3):\n"
            "    return {'answer': 'Backend not yet implemented', 'retrieved_chunks': []}\n\n"
            "def add_document(uploaded_file):\n"
            "    return None\n"
        )
    print("Created backend/rag_pipeline.py (starter template)")
else:
    print("backend/rag_pipeline.py already exists")
