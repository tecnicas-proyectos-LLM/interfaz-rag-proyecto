# Importando librerías
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.messages import HumanMessage

from system_prompts.master_prompt import MASTER_PROMPT
from settings.envs import get_envs

# Cargando variables de entorno
envs = get_envs()

def model_langchain_google_process( input ):
    """
        Esta función contiene la lógica para usar
        un modelo de Google AI con el framework
        de langchain.

        Documentación -> https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai#instantiation
    """
    
    # Instanciando objeto para usar modelo de Google AI
    llm = ChatGoogleGenerativeAI(
        model=envs["google_model_ia"],
        google_api_key=envs["api_key_google"],
        #temperature=0,
        #top_k=None,
        #top_p=None,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    message = [
        (
            "system",
            MASTER_PROMPT,
        ),
        (
            "human",
            input,
        ),
    ]

    response_model = llm.invoke( message )

    return response_model.content