# Importando librerías langchain
from langchain.chat_models import init_chat_model

# Importando variables de entorno
from settings.envs import get_envs

# Importando variables de entorno
envs = get_envs()

def get_setting_model():
    """
        Esta función se encarga de cargar y configurar
        dos modelos que se usarán en el proceso del RAG.

        - Model RAG: es el modelo que se usará para aplicar
        el proceso de RAG.

        - Model summary: es el modelo que se usará para aplicar
        la técnica summary con tal de resumir toda el hilo
        conversacional que se lleva con el modelo. 
    """
    model_RAG = init_chat_model(
        f"google_genai:{ envs["google_model_ia"] }",
        api_key=envs["api_key_google"],
        temperature=0.4,
        timeout=20,
        max_tokens=800,
    )

    model_summary = init_chat_model(
        f"google_genai:{ envs["google_model_ia"] }",
        api_key=envs["api_key_google"],
        temperature=0.6,
        timeout=15,
        max_tokens=400,
    )

    return {
        "model_RAG"    : model_RAG,
        "model_summary": model_summary,
    }

# Obteniendo modelos LLM para todo el proceso
models = get_setting_model()