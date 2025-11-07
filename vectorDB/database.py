# Importando librerías
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from vectorDB.constants import ( PERSIST_DIR, COLLECTION_NAME, OLLAMA_MODEL )

def get_vector_resources():
    """
        Esta función regresa el modelo embedding
        y el objeto de chroma para que se puedan
        usar en otros lados del proyecto.
    """
    model_embeddings = OllamaEmbeddings(
        model=OLLAMA_MODEL,
    )

    chroma_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=model_embeddings,
        persist_directory=PERSIST_DIR,
        collection_metadata={
            "hnsw:space": "cosine",
            "hnsw:search_ef": 50
        }
    )

    return {
        "embedding": model_embeddings,
        "chroma"   : chroma_store,
    }