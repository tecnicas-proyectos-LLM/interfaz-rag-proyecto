# Importando librerías
from ollama import chat
from ollama import ChatResponse

def model_local_process( input ):
    """
        Esta función ejecuta el proceso para 
        interactuar con el modelo local
    """
    message = { 'role': 'user', 'content': input }

    response: ChatResponse = chat(
        model='gemma3:1b',
        messages=[ message ],
    )

    return response.message.content