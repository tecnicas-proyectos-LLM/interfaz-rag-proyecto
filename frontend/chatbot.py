# Importando framework streamlit
import streamlit as st
import base64
import time

def type_effect(content, message_box, delay=0.03):
    """
        Esta función aplica el efecto de typing
        como si el modelo respondiera poco a poco
    """
    placeholder    = message_box.empty()
    displayed_text = ""

    for char in content:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)

def chat_message(role, content):
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

    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        ">
            <img src="data:image/png;base64,{ data }" width="160" style="margin: 0;">
            <p>
                ¡Hola! Soy FVLia, el asistente virtual de la fundación Valle del Lili. Te orientaré en todo
                lo que necesites sobre nuestros servicios y atención al cliente.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def states_chatbot():
    """
        Esta función inicializa el estado para gestionar
        todos los mensajes que sucedan entre el usuario
        y el modelo
    """
    
    # Creando un estado para guardar el historial
    # de las conversaciones
    if "messages_chatbot" not in st.session_state:
        st.session_state["messages_chatbot"] = []

    # Proceso para mostrar todo el historial de conversaciones
    # en la interfaz del chatbot
    for message in st.session_state["messages_chatbot"]:
        role    = message["role"]
        content = message["content"]

        chat_message(role, content)

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

    if "chat_initialized" not in st.session_state:
        chat_message( role='assistant', content=init_message )
        
        # Se coloca una bandera para que no renderice de nuevo el mensaje
        st.session_state["chat_initialized"] = True
        st.session_state["messages_chatbot"].append({
            "role"   : "assistant",
            "content": init_message,
        })

# -----------------------------------------------------------------
# PROCESO PRINCIPAL
# -----------------------------------------------------------------
def init_chatbot( execute_model ):

    # Estableciendo configuraciones principales
    settings_chatbot()
    states_chatbot()
    init_messages_assistant()
    
    # Entrada del usuario
    user_input = st.chat_input("Escribe tu consulta aquí...")

    if user_input:
        # ----------------------------------------------
        # Proceso para guardar entrada usuario en el estado
        # ----------------------------------------------
        st.session_state["messages_chatbot"].append({
            "role"   : "user",
            "content": user_input,
        })

        chat_message( role='user', content=user_input )

        # ----------------------------------------------
        # Proceso para guardar resultado modelo en el estado
        # ----------------------------------------------
        with st.spinner("Espera un momento..."):
            response = execute_model( input=user_input )

        st.session_state["messages_chatbot"].append({
            "role"   : "assistant",
            "content": response,
        })

        chat_message( role='assistant', content=response )

