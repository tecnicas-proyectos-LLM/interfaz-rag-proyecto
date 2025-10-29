# Importando librerías
from openai import (AzureOpenAI)
from pathlib import Path
from settings.envs import get_envs
from system_prompts.master_prompt import MASTER_PROMPT

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

def model_api_process( input ):
    """
        Esta función ejecuta todo el proceso
        API de un modelo privado para empezar
        a interactuar
    """

    # Configurando modelo openAI que está desplegado en Azure
    client = AzureOpenAI(
        api_version=envs["version"],     
        azure_endpoint=envs["endpoint"],
        api_key=envs["api_key"], 
    )
    
    retrieved_context = FIXED_CONTEXT

    # Contenido para el modelo
    messages=[
        {
            "role": "system",
            "content": MASTER_PROMPT,
        },
        {
            "role": "system",
            "content": f"---\n# Contexto recuperado para respuestas:\n{ retrieved_context }",
        },
        {
            "role": "user",
            "content": input,
        },   
    ]

    response = client.chat.completions.create(
        messages=messages,
        max_completion_tokens=16384,
        model=envs["deployment"],
    )
    
    return response.choices[0].message.content
