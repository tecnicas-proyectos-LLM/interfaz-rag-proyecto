# Importando framework streamlit
import streamlit as st
from helpers.uuid import generatorUUID 

import base64

from system_prompts.master_prompt import MASTER_PROMPT
from agent_models.loading import loading_chats
from frontend.presentation_proyect import show_presentation

def chat_message( role, content ):
    """
        Esta función coloca los mensajes
        en la interfaz del chatbot cada vez
        que suceda una interacción
    """    
    assistant_avatar = "frontend/assets/orbe_1.png"

    if role == "assistant":
        #message_box = st.chat_message( role, avatar=assistant_avatar )
        #type_effect( content, message_box, delay=0.005 )
        st.chat_message( role, avatar=assistant_avatar ).markdown( content )
    else:
        st.chat_message( role ).markdown( content )

def settings_chatbot():
    """
        Esta función configura todos los 
        elementos necesarios para el funcionamiento de 
        la interfaz del chatbot con streamlit
    """
    # Se agrega un título e icono en la pestaña del navegador
    st.set_page_config(page_title="FVLia", page_icon="🤖")

    with open("frontend/assets/orbe_1.png", "rb") as file:
        data = base64.b64encode( file.read() ).decode( "utf-8" )

    if not st.session_state.get("presentacion_activa", False):
        st.markdown(
            f"""
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            ">
                <img src="data:image/png;base64,{data}" width="160" style="margin: 0;">
                <p>
                    ¡Hola! Soy FVLia, el asistente virtual de la Fundación Valle del Lili. 
                    Te orientaré en todo lo que necesites sobre nuestros servicios y atención al cliente.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Sidebar
    with st.sidebar:

        st.title("Presentación")
        presentacion_btn = st.button("Ver presentación", icon="🧭")

        # Control de estado de presentación
        if "presentacion_activa" not in st.session_state:
            st.session_state["presentacion_activa"] = False

        if presentacion_btn:
            st.session_state["presentacion_activa"] = True
            st.rerun()

        st.title("Opciones")
        new_chat = st.button("Nuevo chat", icon="✨")

        if new_chat: # Se activa cuando se da click al botón "nuevo chat"
            st.session_state["presentacion_activa"] = False  
            init_new_chat()
            st.rerun()

        st.title("Chats")

        history_chats = st.session_state["chats"]

        if len( history_chats ) != 0:
            for i, chat in enumerate( history_chats ):
                if st.button(f"Messages chat {i+1}"):
                    st.session_state["presentacion_activa"] = False  
                    st.session_state["chat_messages"] = chat["messages"]
                    st.session_state["thread_id"]     = chat["thread_id"]
                    st.rerun()

def states_chatbot():
    """
        Función que inicializa estados para manejarlos
        dentro del proceso de la aplicación.
    """
    # Estado para guardar mensajes durante la interacción
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    # Estado para guardar todos los chat creados
    if "chats" not in st.session_state:
        st.session_state["chats"] = []

    # Estado del ID del hilo global
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generatorUUID()

def init_messages_assistant():
    """
        Esta función muestra un mensaje inicial
        del asistente cuando se ingresa por primera vez
        a la interfaz. Sin embargo, cuando se empieza a 
        interactuar entonces desaparece.
    """
    init_message = """
        ¿Cómo puedo ayudarte hoy?
    """

    if len( st.session_state["chat_messages"] ) == 0:
        """ st.session_state["chat_messages"].append({
            "role"   : "assistant",
            "content": init_message,
        }) """

        chat_message( role='assistant', content=init_message )

def init_new_chat():
    """
        Esta función ejecuta el proceso para
        iniciar un nuevo chat con el modelo LLM.

        previous_chat_messages: es un un arreglo que tiene
        un conjunto de diccionarios con las conversaciones
        entre el modelo y el usuario.
    """
    previous_chat_messages = st.session_state["chat_messages"]

    # Se revisa que al menos haya más de dos mensajes en el chat 
    if len(previous_chat_messages) > 1:
        st.session_state["chats"].append({
            "messages" : previous_chat_messages,
            "thread_id": st.session_state["thread_id"]
        })
        st.session_state["chat_messages"] = []
        st.session_state["thread_id"]     = generatorUUID()

        init_messages_assistant()

# -----------------------------------------------------------------
# PROCESO PRINCIPAL
# -----------------------------------------------------------------
def init_chatbot( execute_model ):
    """
        Este proceso se ejecuta cada vez que se quiera
        interactuar con el modelo.
    """
    states_chatbot()
    loading_chats( state=st.session_state )
    settings_chatbot()

    # Si la presentación está activa, se muestra y se detiene aquí
    if st.session_state.get("presentacion_activa", False):
        show_presentation( st=st, MASTER_PROMPT=MASTER_PROMPT )
        return  # Detiene el flujo del chat

    init_messages_assistant()

    # Proceso para mostrar todo el historial de conversaciones en la interfaz del chatbot
    for message in st.session_state["chat_messages"]:
        role    = message["role"]
        content = message["content"]

        chat_message( role, content )

    # Entrada del usuario
    user_input = st.chat_input("Escribe tu consulta aquí...")

    if user_input:
        # ----------------------------------------------
        # Proceso para guardar entrada usuario en el estado
        # ----------------------------------------------
        st.session_state["chat_messages"].append({
            "role"   : "user",
            "content": user_input,
        })

        chat_message( role='user', content=user_input )

        # ----------------------------------------------
        # Proceso para guardar resultado modelo en el estado
        # ----------------------------------------------
        with st.spinner("Espera un momento..."):
            response = execute_model( input=user_input, thread_id=st.session_state["thread_id"] )

        st.session_state["chat_messages"].append({
            "role"   : "assistant",
            "content": response,
        })

        chat_message( role='assistant', content=response )

