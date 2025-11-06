# Importando otras librerías
from settings.envs import get_envs

# Importando librerías langchain
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres import PostgresSaver 

# Importando Tools y Prompt para el modelo
from tools.tools import ModelTools, prompt_with_context
from system_prompts.master_prompt import MASTER_PROMPT
from langchain.agents import create_agent
from agent_models.model_config import models

# Cargando variables de entorno
envs = get_envs()

# -----------------------------------------------------------------------------
# FUNCIONES PARA CONFIGURACIÓN
def agent_google_shortMemory( input, thread_id ):
    """
        Esta función contiene toda la lógica
        para usar un modelo de Google como Gemini
        con LangChain agent.
    """
    with PostgresSaver.from_conn_string( envs["postgres_url"] ) as checkpointer:
        checkpointer.setup() # De forma automática se crean las tablas en PostgresSQL

        # Instanciando objeto para el agente
        agent = create_agent(
            model=models["model_RAG"],
            tools=[ 
                ModelTools.get_pending_appointments,
                ModelTools.get_contacts_to_schedule,
                ModelTools.get_laboratory_results,
                ModelTools.get_vaccination_programs,
                ModelTools.create_pqrs,
                ModelTools.get_pqrs_status,
            ],
            system_prompt=MASTER_PROMPT,
            middleware=[
                SummarizationMiddleware(
                    model=models["model_summary"],
                    max_tokens_before_summary=4000,
                    messages_to_keep=20,
                ),
                prompt_with_context, # Añadiendo proceso para aplicar RAG
            ],
            checkpointer=checkpointer,
        )

        result = agent.invoke(
            {"messages": [{ "role": "user", "content": f"{ input }" }]},
            {"configurable": {"thread_id": thread_id}},
        )

        # Tomando la última respuesta que corresponde al modelo
        response_model = normalize_content( message=result["messages"][-1] )

        return response_model

def normalize_content( message ):
    """
        Gemini puede regresar respuestas de tipo texto, imágenes, entre otros.
        Por esa razón es necesario organizar la información para que extraer
        el contenido que se mostrará en pantalla. En este caso, sólo se
        trabajará con texto.
    """
    content = message.content

    # Si la respuesta es una lista
    if isinstance( content, list ):
        response = content[0]["text"]
        return response
    
    # Si la respuesta es directamente una cadena
    elif isinstance( content, str ):
        return content
    
    # Si no hay respuesta del modelo
    else:
        return "No hubo respuesta"

# -----------------------------------------------------------------------------
# PROCESO PRINCIPAL
# -----------------------------------------------------------------------------
