# Cargando librerías
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from settings.envs import get_envs

# Cargando variables de entorno
envs = get_envs()

# --- INICIO: Bloque para asegurar la existencia de la base de datos ---
def ensure_db_exists():
    """Asegura que la base de datos exista antes de intentar usarla."""
    try:
        # Intenta conectar a la base de datos especificada
        conn = psycopg.connect(envs["postgres_url"])
        conn.close()
    except psycopg.OperationalError as e:
        # Si la base de datos no existe, se lanza una excepción que contiene "does not exist"
        if "does not exist" in str(e) or "no existe la base de datos" in str(e):
            print("La base de datos no existe. Intentando crearla...")
            db_name = envs["postgres_url"].split("/")[-1]
            # Conéctate al motor de PostgreSQL sin especificar una base de datos (usando la de mantenimiento 'postgres')
            maintenance_conn_str = envs["postgres_url"].replace(f"/{db_name}", "/postgres")
            
            try:
                with psycopg.connect(maintenance_conn_str, autocommit=True) as conn:
                    with conn.cursor() as cur:
                        cur.execute(f'CREATE DATABASE "{db_name}"')
                        print(f"Base de datos '{db_name}' creada exitosamente.")
            except Exception as create_db_e:
                print(f"Error al crear la base de datos: {create_db_e}")
                raise
        else:
            raise

def loading_chats( state ):
    """
        Esta función cargar los chats con 
        sus mensajes correspondientes.
    """
    chats  = []

    # 1. Asegurarse de que la base de datos exista antes de cualquier operación
    ensure_db_exists()

    # 2. Asegurarse de que la tabla "checkpoints" exista
    with PostgresSaver.from_conn_string( envs["postgres_url"] ) as checkpointer:
        checkpointer.setup() # Crea la tabla si no existe

    # 3. Ahora sí, leer los thread_ids de la tabla que ya sabemos que existe
    with psycopg.connect( envs["postgres_url"] ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT thread_id FROM checkpoints")
            thread_ids = [row[0] for row in cur.fetchall()]

    # 4. Consultar los mensajes de cada hilo usando el checkpointer
    with PostgresSaver.from_conn_string( envs["postgres_url"] ) as checkpointer:
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