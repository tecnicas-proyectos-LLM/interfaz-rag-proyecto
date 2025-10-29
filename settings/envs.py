# Importando librerías
from dotenv import load_dotenv
import os

# Cargar variables desde archivo .env al entorno del proyecto
load_dotenv()

def get_envs():
    """
        Función que regresa un objeto con todas
        las variables de entorno del proyecto
    """
    object_envs = {
        "api_key"        : os.getenv("AZURE_OPENAI_API_KEY"),
        "endpoint"       : os.getenv("AZURE_OPENAI_ENDPOINT"),
        "deployment"     : os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "version"        : os.getenv("AZURE_OPENAI_API_VERSION"),
        "api_key_google" : os.getenv("GOOGLE_API_KEY"),
        "google_model_ia": os.getenv("GOOGLE_MODEL_IA"),
        "postgres_url"   : os.getenv("POSTGRES_URL"),
    }
    
    return object_envs