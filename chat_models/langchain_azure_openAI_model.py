# Importando librerías
from settings.envs import get_envs
from langchain_openai import AzureChatOpenAI
from system_prompts.master_prompt import MASTER_PROMPT
from pathlib import Path
import os
import json

# Cargando variables de entorno
envs = get_envs()

def get_fixed_context():
    """
        Esta función toma los chunks y los unifica
        en una sola cadena que recibirá el modelo
        de openAI.
    """
    try:
        base_dir = Path(__file__).resolve().parent  # models/
        file_path = (base_dir.parent / 'chunks' / 'chunks_para_vectorizar-valle_lili_info.json').resolve()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al decodificar el JSON: {e}")
        
        contents = [item.get('content', '') for item in data if isinstance(item, dict)]
        return ' '.join(contents)
    
    except FileNotFoundError:
        print(f"El archivo no existe: {file_path}")
        return ''
    except ValueError:
        print("Error al decodificar el JSON")
        return ''
    except:
        print('error con el contexto')
        return ''

FIXED_CONTEXT = get_fixed_context()

def langchain_azureOpenAI_model( input ):
    """
        Esta función ejecuta la lógica para
        interactuar con un modelo de OpenAI
        desde el entorno de Azure.

        Documentación: https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html#langchain_openai.chat_models.azure.AzureChatOpenAI
    """
    # Configurando modelo
    llm = AzureChatOpenAI(
        azure_deployment=envs["deployment"],
        api_version=envs["version"],
        api_key=envs["api_key"],
        azure_endpoint=envs["endpoint"],
        #temperature=0,
        max_tokens=16384,
        #timeout=None,
        #max_retries=2,
        model="gpt-5-nano",
        #model_version="",
    )

    retrieved_context = FIXED_CONTEXT

    messages = [
        ("system", MASTER_PROMPT),
        ("system", f"---\n# Contexto recuperado para respuestas:\n{ retrieved_context }"),
        ("human", input),
    ]

    response_model = llm.invoke( messages )

    return response_model.content
