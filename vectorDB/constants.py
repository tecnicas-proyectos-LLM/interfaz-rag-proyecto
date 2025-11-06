from pathlib import Path

# Configuración
CHUNKS_FILE = Path(__file__).parent.parent / 'chunks' / 'chunks_valle_de_lili.json'
PROGRESS_FILE = Path(__file__).parent / 'progress.json'
PERSIST_DIR = Path(__file__).parent / 'data'
COLLECTION_NAME = 'valle_lili_context_collection'
OLLAMA_BASE_URL = 'http://localhost:11434'  # Cambia si tu Ollama corre en otra URL
OLLAMA_MODEL = 'embeddinggemma:latest'