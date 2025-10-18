# Importando librerías
import os
import json
from langchain_ollama import ChatOllama
from system_prompts.master_prompt import MASTER_PROMPT

def get_fixed_context():
    try:
        file_path = '../chunks/chunks_para_vectorizar-valle_lili_info.json'
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al decodificar el JSON: {e}")
        
        contents = [item.get('content', '') for item in data if isinstance(item, dict)]
        return ' '.join(contents)
    except:
        return ''


FIXED_CONTEXT = get_fixed_context()

def model_langchain_process( input ):
    """
        Esta función ejecuta el uso de un modelo
        instalado en el gestor de ollama usando
        el framework de langchain
    """
    llm_instance = ChatOllama(
        model="gemma3:1b",
        validate_model_on_init=True,
        temperature=0.8,
        #num_predict=500,
        #stop=[],
        #reasoning=False,
    )

    retrieved_context = FIXED_CONTEXT
    print(len(FIXED_CONTEXT))

    messages = [
        ("system", MASTER_PROMPT),
        ("system", f"---\n# Contexto recuperado para respuestas:\n{retrieved_context}"),
        ("user", input),
    ]

    response_model = llm_instance.invoke( messages )

    return response_model.content
