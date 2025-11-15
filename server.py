from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from agent_models.google_model_shortMemory import agent_google_shortMemory

app = FastAPI()

def run_agent(input_data):
    """
    LangServe envía SOLO el valor del campo 'input'.
    Así que input_data ya es directamente:
    {
        "text": "...",
        "thread_id": "..."
    }
    """
    if not isinstance(input_data, dict):
        raise ValueError("El input debe ser un dict con 'text' y 'thread_id'.")

    text = input_data.get("text")
    thread_id = input_data.get("thread_id")

    if not text:
        raise ValueError("Falta 'text' en el input.")
    if not thread_id:
        raise ValueError("Falta 'thread_id' en el input.")

    return agent_google_shortMemory(
        input=text,
        thread_id=thread_id
    )

agente = RunnableLambda(run_agent)

add_routes(app, agente, path="/agent")
