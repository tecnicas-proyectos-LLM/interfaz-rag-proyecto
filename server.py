from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from agent_models.google_model_shortMemory import agent_google_shortMemory
from helpers.uuid import generatorUUID

app = FastAPI()

def run_agent(input_text: str):
    return agent_google_shortMemory(input=input_text, thread_id=generatorUUID())

# Convertimos tu función en un Runnable real
agente = RunnableLambda(run_agent)

# Exponemos la ruta
add_routes(app, agente, path="/agent")


"""
uv run uvicorn server:app --host 0.0.0.0 --port 8000
POST http://localhost:8000/agent/invoke
Body:
{
  "input": "Dame el esquema de vacunación para un niño de 5 años"
}
"""