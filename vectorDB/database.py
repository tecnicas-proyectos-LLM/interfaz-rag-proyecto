# Importando librerías
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def get_vector_resources():
    """
        Esta función regresa el modelo embedding
        y el objeto de chroma para que se puedan
        usar en otros lados del proyecto.
    """
    model_embeddings = OllamaEmbeddings(
        model="embeddinggemma",
    )

    chroma_store = Chroma(
        collection_name="example_collection",
        embedding_function=model_embeddings,
        persist_directory="./vectorDB/data"
    )

    return {
        "embedding": model_embeddings,
        "chroma"   : chroma_store,
    }