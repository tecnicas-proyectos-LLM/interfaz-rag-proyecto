# Importando otras librerías
from settings.envs import get_envs

# Importando librerías langchain
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
#from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver 

# Importando Tools para el modelo
from tools.tools import ModelTools

# Cargando variables de entorno
envs = get_envs()

def get_setting_model():
    """
        Esta función se encarga de cargar el modelo
        con las configuraciones necesarias para
        su funcionamiento
    """
    model = init_chat_model(
        f"google_genai:{ envs["google_model_ia"] }",
        api_key=envs["api_key_google"],
        #temperature=0.5,
        #timeout=10,
        #max_tokens=1000,
    )

    return model

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

def agent_google_shortMemory( input ):
    """
        Esta función contiene toda la lógica
        para usar un modelo de Google como Gemini
        con LangChain agent.
    """
    #TODO: falta implementar la estrategía summary para resumir las conversaciones guardadas
    with PostgresSaver.from_conn_string( envs["postgres_url"] ) as checkpointer:
        checkpointer.setup() # De forma automática se crean las tables en PostgresSQL

        # Instanciando objeto para el agente
        agent = create_agent(
            model=get_setting_model(),
            tools=[ ModelTools.get_weather ],
            system_prompt="Tu eres un asistente",
            checkpointer=checkpointer,
        )

        result = agent.invoke(
            {"messages": [{ "role": "user", "content": f"{ input }" }]},
            {"configurable": {"thread_id": "1"}},
        )

        # Tomando la última respuesta que corresponde al modelo
        response_model = normalize_content( message=result["messages"][-1] )

        return response_model