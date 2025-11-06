"""Script para vectorizar los chunks usando Ollama (embeddinggemma:latest)

Este archivo procesa el JSON de chunks, crea embeddings con Ollama
(`embeddinggemma:latest`) y los guarda en una colección Chroma local.
Soporta reanudado mediante `progress.json` y procesa en batches con
reintentos básicos.
"""

import json
import time
from uuid import uuid4
from typing import List

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from vectorDB.constants import (
    CHUNKS_FILE,
    PROGRESS_FILE,
    PERSIST_DIR,
    COLLECTION_NAME,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL
)


def save_progress(last_processed_index: int, total_documents: int):
    """Guarda el progreso actual en PROGRESS_FILE"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'last_processed_index': last_processed_index,
            'total_documents': total_documents,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f)


def load_progress():
    """Carga último progreso guardado (si existe)"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'last_processed_index': 0, 'total_documents': 0}


def build_chroma_with_ollama():
    emb = OllamaEmbeddings(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
    chroma_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=emb,
        persist_directory=str(PERSIST_DIR),
        collection_metadata={
            "hnsw:space": "cosine",  # ← CRÍTICO
            "hnsw:search_ef": 50     # ← Mejora recall
        }
    )
    return chroma_store



def process_batch(documents: List[Document], uuids: List[str], chroma_db, batch_size: int = 64):
    """Procesa los documentos en batches y persiste tras cada batch.

    batch_size por defecto es 64 (ajusta según memoria y rendimiento).
    """
    total = len(documents)
    total_batches = total // batch_size + (1 if total % batch_size else 0)

    for i in range(0, total, batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_uuids = uuids[i:i + batch_size]
        batch_no = i // batch_size + 1
        print(f"Procesando batch {batch_no}/{total_batches} (docs {i}-{i+len(batch_docs)-1})...")
        try:
            chroma_db.add_documents(documents=batch_docs, ids=batch_uuids)

            # Guardar progreso (siguiente índice a procesar)
            save_progress(i + len(batch_docs), total)
            print(f"Batch {batch_no} completado.")
            # Pequeña pausa para evitar saturar recursos locales
            time.sleep(0.1)
        except Exception as e:
            print(f"Error en batch {batch_no}: {e}")
            print("Guardando progreso y abortando para reintentar después.")
            save_progress(i, total)
            return False

    # Si llegamos aquí, terminamos con éxito
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
    return True


def vectorize_context_chunks():
    """Función principal: carga chunks, crea documentos y los almacena en Chroma usando Ollama."""
    progress = load_progress()
    start_index = progress.get('last_processed_index', 0)

    if start_index > 0:
        print(f"Reanudando desde el índice {start_index}...")

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo de chunks: {CHUNKS_FILE}")

    print("Cargando chunks desde el archivo JSON...")
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    print("Chunks cargados con éxito.")

    print("Convirtiendo chunks a documentos de LangChain...")
    documents: List[Document] = []
    for chunk in chunks_data:
        doc_content = chunk.get('content', '')
        doc_metadata = chunk.get('metadata', {})
        titulo = doc_metadata.get('title', '')
        doc = Document(page_content=f"{titulo}\n{doc_content}", metadata=chunk.get('metadata', {}))
        documents.append(doc)

    total_docs = len(documents)
    if start_index >= total_docs:
        print("Todos los documentos ya han sido procesados.")
        return

    remaining = documents[start_index:]
    uuids = [str(uuid4()) for _ in range(total_docs)][start_index:]

    print(f"Total de documentos: {total_docs}")
    print(f"Documentos restantes: {len(remaining)}")

    print("Construyendo Chroma con Ollama embeddings...")
    chroma_store = build_chroma_with_ollama()

    print("Iniciando procesamiento por batches...")
    success = process_batch(remaining, uuids, chroma_store, batch_size=64)

    if success:
        print("Vectorización completada con éxito.")
    else:
        print("Proceso interrumpido. Ejecuta de nuevo para reanudar desde el último progreso.")


if __name__ == '__main__':
    vectorize_context_chunks()