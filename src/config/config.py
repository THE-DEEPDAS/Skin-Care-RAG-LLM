import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Storage configurations
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "vectordb")
DOCUMENTS_PATH = os.path.join(BASE_DIR, "storage", "documents")

# Model configurations
MODEL_NAME = "llama2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_BASE_URL = "http://localhost:11434"

# API configurations
API_PORT = 5000
