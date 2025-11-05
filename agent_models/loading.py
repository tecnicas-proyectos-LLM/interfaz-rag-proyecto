# Cargando librerías
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from settings.envs import get_envs

# Cargando variables de entorno
envs = get_envs()

def loading_chats( state ):
    """
        Esta función cargar los chats con 
        sus mensajes correspondientes.
    """
    chats  = []

    # Se busca directamente en la BD todos los thread_IDS guardados
    with psycopg.connect( envs["postgres_url"] ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT thread_id FROM checkpoints")
            thread_ids = [row[0] for row in cur.fetchall()]

    # Se consulta la BD con métodos especiales que tiene PostgresSaver
    with PostgresSaver.from_conn_string( envs["postgres_url"] ) as checkpointer:
        checkpointer.setup() # De forma automática se crean las tables en PostgresSQL

        # Consultando todos los mensajes de cada thread (hilo)
        for thread_id in thread_ids:
            states   = checkpointer.get({"configurable": {"thread_id": f"{thread_id}"}})
            messages = []
            
            for message in states["channel_values"]["messages"]:
                # Se revisa si el mensaje pertenece a: user, model o tool
                if isinstance(message, HumanMessage):
                    role = "user"
                elif isinstance(message, AIMessage):
                    role = "assistant"
                elif isinstance(message, ToolMessage):
                    role = "tool"
                
                # Se omiten ciertos mensajes que no son necesarios
                if role == "tool":
                    continue

                if role == "assistant" and message.content == '':
                    continue

                if role == "assistant":
                    # Si la respuesta es una lista
                    if isinstance( message.content, list ):
                        messages.append({
                            "role"   : role,
                            "content": message.content[0]["text"],
                        })
                    else:                       
                        messages.append({
                            "role"   : role,
                            "content": message.content,
                        })
                    
                    continue

                # Guardando mensaje del thread
                messages.append({
                    "role"   : role,
                    "content": message.content,
                })
            
            chats.append({
                "messages" : messages,
                "thread_id": thread_id,
            })
    
    # Guardando chats en el estado de streamlit correspondiente
    state["chats"] = chats