# Importando librerías
from langchain_ollama import ChatOllama

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

    messages = [
        ("system", "Sé un asistente experto en cualquier tema"),
        ("human", input),
    ]

    response_model = llm_instance.invoke( messages )

    return response_model.content