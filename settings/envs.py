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
        "api_key"   : os.getenv("AZURE_OPENAI_API_KEY"),
        "endpoint"  : os.getenv("AZURE_OPENAI_ENDPOINT"),
        "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "version"   : os.getenv("AZURE_OPENAI_API_VERSION"),
    }
    
    return object_envs